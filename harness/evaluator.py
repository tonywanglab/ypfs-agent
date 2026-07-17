"""Direct rubric judge for completed agent runs."""

from __future__ import annotations

import json

from . import config, llm
from .models import CheckResult, CriterionVerdict, Judgment, RubricVersion
from .storage import new_id, now_iso
from .trace import NormalizedTrace


JUDGE_SYSTEM_PROMPT = """\
You are an independent judge for a financial-crisis policy research agent.
Evaluate the supplied answer strictly against every supplied LLM rubric
criterion. The rubric is the complete definition of answer quality; do not
invent additional criteria or rewrite it.

Use the agent trace only as evidence about retrieval and tool use. Deterministic
check results are authoritative and are scored separately.

Respond with ONLY a JSON object:
{
  "criteria": [
    {"criterion_id": "<exact supplied id>",
     "verdict": "pass" | "fail" | "uncertain",
     "evidence": "<short quote or concrete explanation>",
     "confidence": <0-1 float>}
  ],
  "summary": "<2-4 sentence overall assessment>",
  "failure_feedback": "<concrete improvement; empty if none>"
}
Return exactly one entry for every supplied LLM criterion_id.
"""


def _deterministic_verdicts(
    rubric: RubricVersion,
    check_results: list[CheckResult],
) -> dict[str, CriterionVerdict]:
    results_by_id = {result.check_id: result for result in check_results}
    verdicts: dict[str, CriterionVerdict] = {}
    for criterion in rubric.criteria:
        if criterion.check_type != "deterministic":
            continue
        result = results_by_id.get(criterion.deterministic_check)
        if result is None:
            verdicts[criterion.id] = CriterionVerdict(
                criterion_id=criterion.id,
                verdict="uncertain",
                evidence=f"No deterministic result for {criterion.deterministic_check!r}.",
                confidence=0.0,
                source="deterministic",
            )
            continue
        verdicts[criterion.id] = CriterionVerdict(
            criterion_id=criterion.id,
            verdict="pass" if result.passed else "fail",
            evidence=result.evidence,
            confidence=1.0,
            source="deterministic",
        )
    return verdicts


def judge_answer(
    case_prompt: str,
    answer: str,
    normalized_trace: NormalizedTrace,
    rubric: RubricVersion,
    check_results: list[CheckResult],
    run_id: str,
) -> Judgment:
    deterministic = _deterministic_verdicts(rubric, check_results)
    llm_criteria = [criterion for criterion in rubric.criteria if criterion.check_type == "llm"]
    llm_verdicts: dict[str, CriterionVerdict] = {}
    summary = ""
    failure_feedback = ""
    model = config.judge_model()

    if llm_criteria:
        payload = {
            "question": case_prompt,
            "rubric_criteria": [criterion.to_dict() for criterion in llm_criteria],
            "agent_answer": answer,
            "agent_retrieved_doc_ids": sorted(normalized_trace.retrieved_doc_ids),
            "agent_fetched_doc_ids": sorted(normalized_trace.fetched_doc_ids),
            "agent_tool_errors": normalized_trace.tool_errors,
            "deterministic_check_results": [
                result.to_dict() for result in check_results
            ],
        }
        try:
            parsed = llm.chat_json(
                system_prompt=JUDGE_SYSTEM_PROMPT,
                user_prompt=json.dumps(payload, indent=2, default=str),
                model=model,
            )
        except llm.LLMError as exc:
            parsed = {
                "criteria": [],
                "summary": "Judge output was malformed; LLM criteria are uncertain.",
                "failure_feedback": str(exc),
            }
        valid_ids = {criterion.id for criterion in llm_criteria}
        raw_criteria = parsed.get("criteria", [])
        if not isinstance(raw_criteria, list):
            raw_criteria = []
        for raw in raw_criteria:
            if not isinstance(raw, dict):
                continue
            criterion_id = raw.get("criterion_id")
            if criterion_id not in valid_ids or criterion_id in llm_verdicts:
                continue
            verdict = raw.get("verdict", "uncertain")
            if verdict not in ("pass", "fail", "uncertain"):
                verdict = "uncertain"
            try:
                confidence = max(0.0, min(1.0, float(raw.get("confidence", 0.5))))
            except (TypeError, ValueError):
                confidence = 0.5
            llm_verdicts[criterion_id] = CriterionVerdict(
                criterion_id=criterion_id,
                verdict=verdict,
                evidence=str(raw.get("evidence", "")),
                confidence=confidence,
                source="llm",
            )
        summary = str(parsed.get("summary", ""))
        failure_feedback = str(parsed.get("failure_feedback", ""))

    ordered: list[CriterionVerdict] = []
    for criterion in rubric.criteria:
        if criterion.id in deterministic:
            ordered.append(deterministic[criterion.id])
        elif criterion.id in llm_verdicts:
            ordered.append(llm_verdicts[criterion.id])
        else:
            ordered.append(CriterionVerdict(
                criterion_id=criterion.id,
                verdict="uncertain",
                evidence="Judge did not return a verdict for this criterion.",
                confidence=0.0,
                source="llm",
            ))

    return Judgment(
        judgment_id=new_id("judg"),
        run_id=run_id,
        model=model,
        criteria=ordered,
        summary=summary,
        failure_feedback=failure_feedback,
        created_at=now_iso(),
    )
