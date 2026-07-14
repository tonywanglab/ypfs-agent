"""Deterministic, pure gate checks over (answer, messages).

These never call a model and never touch the network. A hard_failure blocks
promotion outright, but the judge still runs afterward so the update loop
gets a full diagnostic picture rather than a truncated one.

Citation detection uses the corpus's doc_id shape (volN_issM_K) directly in
the answer text rather than a specific bracket format, since the current
agent/system_prompt.md does not mandate one — this keeps the checks robust
to prompt wording changes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .models import CheckResult
from .trace import MAX_STEPS_SENTINEL, NormalizedTrace, normalize_messages

REPO_ROOT = Path(__file__).resolve().parent.parent
METADATA_DIR = REPO_ROOT / "metadata"

DOC_ID_PATTERN = re.compile(r"\bvol\d+_iss\d+_\d+\b")

_METADATA_CACHE: dict[tuple[Path, str], dict | None] = {}


def _load_metadata(doc_id: str, metadata_dir: Path = METADATA_DIR) -> dict | None:
    key = (metadata_dir, doc_id)
    if key not in _METADATA_CACHE:
        path = metadata_dir / f"{doc_id}.json"
        _METADATA_CACHE[key] = json.loads(path.read_text()) if path.exists() else None
    return _METADATA_CACHE[key]


def extract_cited_doc_ids(answer: str) -> list[str]:
    """All doc_id-shaped tokens mentioned in the answer, in order, deduped."""
    seen: list[str] = []
    for m in DOC_ID_PATTERN.finditer(answer or ""):
        if m.group(0) not in seen:
            seen.append(m.group(0))
    return seen


def check_completed_cleanly(answer: str, trace: NormalizedTrace) -> CheckResult:
    if trace.hit_max_steps:
        return CheckResult(
            check_id="completed_without_error", passed=False, hard_failure=True,
            evidence=f"Answer is the MAX_STEPS sentinel: {MAX_STEPS_SENTINEL!r}",
        )
    if trace.tool_errors:
        names = ", ".join(sorted({e["tool_name"] for e in trace.tool_errors}))
        return CheckResult(
            check_id="completed_without_error", passed=False, hard_failure=True,
            evidence=f"{len(trace.tool_errors)} tool error(s) from: {names}",
            detail={"tool_errors": trace.tool_errors},
        )
    if not (answer or "").strip():
        return CheckResult(
            check_id="completed_without_error", passed=False, hard_failure=True,
            evidence="Answer is empty.",
        )
    return CheckResult(
        check_id="completed_without_error", passed=True, hard_failure=False,
        evidence="Answer is non-empty; no tool errors; did not hit MAX_STEPS.",
    )


def check_no_survey_citations(answer: str, trace: NormalizedTrace,
                               metadata_dir: Path = METADATA_DIR) -> CheckResult:
    cited = extract_cited_doc_ids(answer)
    survey_cites = [
        doc_id for doc_id in cited
        if (meta := _load_metadata(doc_id, metadata_dir)) and meta.get("document_type") == "survey"
    ]
    if survey_cites:
        return CheckResult(
            check_id="no_survey_citations", passed=False, hard_failure=True,
            evidence=f"Cited survey document(s): {', '.join(survey_cites)}",
            detail={"survey_cites": survey_cites},
        )
    return CheckResult(
        check_id="no_survey_citations", passed=True, hard_failure=False,
        evidence=(f"No survey citations among {len(cited)} cited doc_id(s)." if cited
                  else "No doc_id citations detected in the answer."),
    )


def check_citations_resolve(answer: str, trace: NormalizedTrace,
                             metadata_dir: Path = METADATA_DIR) -> CheckResult:
    cited = extract_cited_doc_ids(answer)
    seen_doc_ids = trace.retrieved_doc_ids | trace.fetched_doc_ids
    unknown = [d for d in cited if _load_metadata(d, metadata_dir) is None]
    not_in_trace = [d for d in cited if d not in unknown and d not in seen_doc_ids]

    if unknown:
        return CheckResult(
            check_id="citations_resolve", passed=False, hard_failure=True,
            evidence=f"Cited doc_id(s) with no corpus metadata: {', '.join(unknown)}",
            detail={"unknown": unknown},
        )
    if not_in_trace:
        return CheckResult(
            check_id="citations_resolve", passed=False, hard_failure=True,
            evidence=(f"Cited doc_id(s) never retrieved or fetched in this run: "
                      f"{', '.join(not_in_trace)}"),
            detail={"not_in_trace": not_in_trace},
        )
    return CheckResult(
        check_id="citations_resolve", passed=True, hard_failure=False,
        evidence=(f"All {len(cited)} cited doc_id(s) resolve to metadata and were "
                  f"retrieved/fetched in-trace." if cited
                  else "No doc_id citations to verify."),
    )


# Maps a Rubric criterion's `deterministic_check` field (== CheckResult.check_id)
# to its implementation, so the judge can look up and copy verdicts in
# verbatim for deterministic criteria without re-deriving them.
CHECKS_BY_ID = {
    "completed_without_error": check_completed_cleanly,
    "no_survey_citations": check_no_survey_citations,
    "citations_resolve": check_citations_resolve,
}


def run_checks(answer: str, messages: list[dict],
                metadata_dir: Path = METADATA_DIR) -> tuple[list[CheckResult], NormalizedTrace]:
    """Run every deterministic check against one (answer, messages) pair."""
    trace = normalize_messages(messages, answer=answer)
    results = [
        check_completed_cleanly(answer, trace),
        check_no_survey_citations(answer, trace, metadata_dir),
        check_citations_resolve(answer, trace, metadata_dir),
    ]
    return results, trace


def any_hard_failure(results: list[CheckResult]) -> bool:
    return any(r.hard_failure and not r.passed for r in results)
