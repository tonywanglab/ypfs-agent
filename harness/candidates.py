"""Update-loop proposal generation and manual approval.

Two branches, never both in the same cycle (enforced by harness.registry):

  rubric branch  — supervisor reviews with failure_attribution in
                   {rubric_gap, judge_failure} -> propose_rubric -> approve
  prompt branch  — supervisor reviews with failure_attribution == agent_failure
                   -> propose_prompt -> A/B -> promote

Proposals are LLM-generated drafts the supervisor edits before approving.
Nothing is promoted automatically.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable

from . import llm, registry, reviews
from .checks import CHECKS_BY_ID
from .models import PromptVersion, Rubric, RubricCriterion
from .runner import load_run_bundle
from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json

RUBRICS_DIR = EVALS_DIR / "rubrics"
PROPOSALS_DIR = RUBRICS_DIR / "proposals"
PROMPTS_DIR = EVALS_DIR / "prompts"
CANDIDATES_DIR = PROMPTS_DIR / "candidates"


RUBRIC_PROPOSAL_SYSTEM = """\
You propose updates to a frozen evaluation rubric for a financial-crisis \
policy research agent. Given the current rubric and supervisor feedback, \
produce a revised rubric that better captures what the expert cares about.

Respond with ONLY a JSON object:
{
  "rationale": "<why these changes>",
  "criteria": [
    {"id": "<stable snake_case id>",
     "description": "<criterion text>",
     "check_type": "llm" | "deterministic",
     "weight": 1.0,
     "deterministic_check": "<only for deterministic: one of "
       "no_survey_citations | citations_resolve | completed_without_error>"}
  ]
}
Keep existing criterion ids when the criterion still applies; add or refine \
as needed. Do not remove deterministic citation/completion checks unless \
the supervisor explicitly says they are wrong.
"""

PROMPT_PROPOSAL_SYSTEM = """\
You propose a revised system prompt for a financial-crisis policy research \
agent. Given the current active prompt and supervisor feedback on agent \
failures, produce an improved prompt that addresses the concrete problems \
raised — without changing the agent's tools or retrieval backend.

Respond with ONLY a JSON object:
{
  "rationale": "<why these changes>",
  "text": "<full revised system prompt markdown>"
}
Preserve the source hierarchy (surveys shape reasoning but are not cited; \
case studies are primary citation targets) and the plan output format unless \
the supervisor says otherwise.
"""


def load_rubric(rubric_id: str) -> Rubric:
    return Rubric.from_dict(read_json(RUBRICS_DIR / f"{rubric_id}.json"))


def load_prompt(prompt_id: str) -> PromptVersion:
    return PromptVersion.from_dict(read_json(PROMPTS_DIR / f"{prompt_id}.json"))


def load_prompt_version(prompt_id: str) -> PromptVersion:
    """Load an active/archived prompt or a candidate from evals/prompts/."""
    for directory in (PROMPTS_DIR, CANDIDATES_DIR):
        path = directory / f"{prompt_id}.json"
        if path.exists():
            return PromptVersion.from_dict(read_json(path))
    raise FileNotFoundError(f"Prompt {prompt_id!r} not found under {PROMPTS_DIR}")


def load_prompt_candidate(prompt_id: str) -> PromptVersion:
    """Load only from the editable candidate store."""
    return PromptVersion.from_dict(
        read_json(CANDIDATES_DIR / f"{prompt_id}.json")
    )


def require_current_prompt_candidate(prompt_id: str) -> PromptVersion:
    candidate = load_prompt_candidate(prompt_id)
    if candidate.status != "candidate":
        raise ValueError(f"Prompt {prompt_id} is not in candidate status")
    _require_artifact_cycle("prompt", candidate.cycle_id)
    if registry.active_prompt_id() != candidate.parent_prompt_id:
        raise ValueError(
            f"Prompt {prompt_id} is stale because its parent prompt is no longer active"
        )
    return candidate


def load_proposal(proposal_id: str) -> Rubric:
    return Rubric.from_dict(read_json(PROPOSALS_DIR / f"{proposal_id}.json"))


def list_rubrics() -> list[Rubric]:
    if not RUBRICS_DIR.exists():
        return []
    return [
        Rubric.from_dict(read_json(p))
        for p in sorted(RUBRICS_DIR.glob("rubric_v*.json"))
        if p.is_file()
    ]


def list_proposals() -> list[Rubric]:
    if not PROPOSALS_DIR.exists():
        return []
    return [
        Rubric.from_dict(read_json(p))
        for p in sorted(PROPOSALS_DIR.glob("*.json"))
    ]


def list_prompt_candidates() -> list[PromptVersion]:
    if not CANDIDATES_DIR.exists():
        return []
    return [
        PromptVersion.from_dict(read_json(p))
        for p in sorted(CANDIDATES_DIR.glob("*.json"))
    ]


def _next_rubric_version() -> int:
    versions = [r.version for r in list_rubrics() + list_proposals()]
    return max(versions, default=0) + 1


def _next_prompt_version() -> int:
    versions = [p.version for p in [load_prompt(registry.active_prompt_id())]
                + list_prompt_candidates()]
    return max(versions, default=0) + 1


def _review_context(review_ids: list[str]) -> list[dict]:
    ctx = []
    for rid in review_ids:
        review = reviews.load_review(rid)
        bundle = load_run_bundle(review.run_id)
        ctx.append({
            "review": review.to_dict(),
            "judgment_summary": bundle["judgment"].get("summary", ""),
            "failure_feedback": bundle["judgment"].get("failure_feedback", ""),
            "checks": bundle["checks"],
        })
    return ctx


def _release_failed_cycle(
    branch: registry.Branch,
    cycle_id: str,
    opened: bool,
    cause: Exception,
) -> None:
    if opened:
        try:
            registry.close_cycle(
                decision="failed",
                expected_branch=branch,
                expected_cycle_id=cycle_id,
            )
        except Exception as cleanup_error:
            cause.add_note(f"Failed to release {branch} cycle: {cleanup_error}")


def _attempt_rollback(cause: Exception, description: str, action: Callable[[], None]) -> None:
    try:
        action()
    except Exception as rollback_error:
        cause.add_note(f"Failed to {description}: {rollback_error}")


def _require_artifact_cycle(branch: registry.Branch, cycle_id: str | None) -> None:
    if cycle_id is None:
        raise ValueError("Artifact is missing its review cycle identity")
    registry.require_cycle(branch, cycle_id=cycle_id)


def propose_rubric(review_ids: list[str], model: str, *, opened_by: str = "supervisor") -> Rubric:
    """Generate a rubric proposal from supervisor reviews. Locks the rubric
    branch for this cycle; raises CycleLockedError if the prompt branch is
    already open."""
    cycle, opened = registry.open_cycle("rubric", opened_by=opened_by)
    cycle_id = cycle["cycle"]["cycle_id"]
    try:
        parent = load_rubric(registry.active_rubric_id())
        payload = {
            "parent_rubric": parent.to_dict(),
            "supervisor_feedback": _review_context(review_ids),
        }
        parsed = llm.chat_json(
            RUBRIC_PROPOSAL_SYSTEM,
            json.dumps(payload, indent=2, default=str),
            model,
        )
        version = _next_rubric_version()
        criteria = _criteria_from_data(parsed.get("criteria", []))
        proposal = Rubric(
            rubric_id=f"rubric_v{version}_prop_{new_id('')}",
            version=version,
            status="proposed",
            criteria=criteria,
            created_at=now_iso(),
            parent_rubric_id=parent.rubric_id,
            rationale=parsed.get("rationale", ""),
            derived_from_review_ids=review_ids,
            cycle_id=cycle_id,
        )
        PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
        atomic_write_json(PROPOSALS_DIR / f"{proposal.rubric_id}.json", proposal.to_dict())
        return proposal
    except Exception as exc:
        _release_failed_cycle("rubric", cycle_id, opened, exc)
        raise


def propose_prompt(review_ids: list[str], model: str, *, opened_by: str = "supervisor") -> PromptVersion:
    """Generate a prompt candidate from agent_failure reviews."""
    cycle, opened = registry.open_cycle("prompt", opened_by=opened_by)
    cycle_id = cycle["cycle"]["cycle_id"]
    try:
        parent = load_prompt(registry.active_prompt_id())
        payload = {
            "parent_prompt": parent.to_dict(),
            "supervisor_feedback": _review_context(review_ids),
        }
        parsed = llm.chat_json(
            PROMPT_PROPOSAL_SYSTEM,
            json.dumps(payload, indent=2, default=str),
            model,
        )
        text = parsed.get("text", parent.text)
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Prompt text must be a non-empty string")
        version = _next_prompt_version()
        candidate = PromptVersion(
            prompt_id=f"prompt_v{version}_{new_id('')}",
            version=version,
            status="candidate",
            text=text,
            created_at=now_iso(),
            parent_prompt_id=parent.prompt_id,
            rationale=parsed.get("rationale", ""),
            derived_from_review_ids=review_ids,
            cycle_id=cycle_id,
        )
        CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        atomic_write_json(CANDIDATES_DIR / f"{candidate.prompt_id}.json", candidate.to_dict())
        return candidate
    except Exception as exc:
        _release_failed_cycle("prompt", cycle_id, opened, exc)
        raise


def _criteria_from_data(data) -> list[RubricCriterion]:
    if not isinstance(data, list) or not data:
        raise ValueError("A rubric must contain at least one criterion")

    criteria = []
    seen_ids = set()
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Criterion {index + 1} must be a JSON object")
        criterion_id = item.get("id")
        description = item.get("description")
        check_type = item.get("check_type", "llm")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise ValueError(f"Criterion {index + 1} must have a non-empty id")
        if criterion_id in seen_ids:
            raise ValueError(f"Duplicate criterion id: {criterion_id}")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"Criterion {criterion_id} must have a non-empty description")
        if check_type not in ("llm", "deterministic"):
            raise ValueError(f"Criterion {criterion_id} has invalid check_type {check_type!r}")
        try:
            weight = float(item.get("weight", 1.0))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Criterion {criterion_id} has an invalid weight") from exc
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError(f"Criterion {criterion_id} weight must be finite and positive")

        deterministic_check = item.get("deterministic_check")
        if check_type == "deterministic" and deterministic_check not in CHECKS_BY_ID:
            raise ValueError(
                f"Criterion {criterion_id} must name a supported deterministic check"
            )
        if check_type == "llm":
            deterministic_check = None

        seen_ids.add(criterion_id)
        criteria.append(RubricCriterion(
            id=criterion_id,
            description=description,
            check_type=check_type,
            weight=weight,
            deterministic_check=deterministic_check,
        ))
    return criteria


def _parse_criteria_json(text: str) -> list[RubricCriterion]:
    return _criteria_from_data(json.loads(text))


def approve_rubric(proposal_id: str, criteria_json: str | None = None) -> Rubric:
    with registry.transaction():
        return _approve_rubric(proposal_id, criteria_json)


def _approve_rubric(proposal_id: str, criteria_json: str | None = None) -> Rubric:
    """Freeze a proposal as the new active rubric version."""
    proposal = Rubric.from_dict(read_json(PROPOSALS_DIR / f"{proposal_id}.json"))
    if proposal.status != "proposed":
        raise ValueError(f"Proposal {proposal_id} is not in proposed status")
    _require_artifact_cycle("rubric", proposal.cycle_id)
    if registry.active_rubric_id() != proposal.parent_rubric_id:
        raise ValueError(
            f"Proposal {proposal_id} is stale because its parent rubric is no longer active"
        )

    criteria = (
        _parse_criteria_json(criteria_json)
        if criteria_json is not None
        else _criteria_from_data([criterion.to_dict() for criterion in proposal.criteria])
    )
    frozen_id = re.sub(r"_prop_[a-f0-9]+$", "", proposal.rubric_id)
    if frozen_id == proposal.rubric_id:
        frozen_id = f"rubric_v{proposal.version}"

    frozen = Rubric(
        rubric_id=frozen_id,
        version=proposal.version,
        status="frozen",
        criteria=criteria,
        created_at=now_iso(),
        parent_rubric_id=proposal.parent_rubric_id,
        rationale=proposal.rationale,
        derived_from_review_ids=proposal.derived_from_review_ids,
        cycle_id=proposal.cycle_id,
    )
    frozen_path = RUBRICS_DIR / f"{frozen.rubric_id}.json"
    if frozen_path.exists():
        raise ValueError(f"Frozen rubric {frozen.rubric_id} already exists")

    activated = False
    consumed = False
    try:
        atomic_write_json(frozen_path, frozen.to_dict())
        registry.set_active_rubric(frozen.rubric_id)
        activated = True
        proposal.status = "rejected"  # proposal artifact kept but marked consumed
        atomic_write_json(PROPOSALS_DIR / f"{proposal_id}.json", proposal.to_dict())
        consumed = True
        registry.close_cycle(
            decision="approved",
            expected_branch="rubric",
            expected_cycle_id=proposal.cycle_id,
        )
        return frozen
    except Exception as exc:
        if consumed:
            proposal.status = "proposed"
            _attempt_rollback(
                exc,
                "restore proposed rubric status",
                lambda: atomic_write_json(
                    PROPOSALS_DIR / f"{proposal_id}.json",
                    proposal.to_dict(),
                ),
            )
        if activated:
            _attempt_rollback(
                exc,
                "restore active rubric",
                lambda: registry.set_active_rubric(proposal.parent_rubric_id),
            )
        _attempt_rollback(
            exc,
            "remove incomplete frozen rubric",
            lambda: frozen_path.unlink(missing_ok=True),
        )
        raise


def deny_rubric(proposal_id: str) -> Rubric:
    with registry.transaction():
        return _deny_rubric(proposal_id)


def _deny_rubric(proposal_id: str) -> Rubric:
    proposal = Rubric.from_dict(read_json(PROPOSALS_DIR / f"{proposal_id}.json"))
    if proposal.status != "proposed":
        raise ValueError(f"Proposal {proposal_id} is not in proposed status")
    _require_artifact_cycle("rubric", proposal.cycle_id)
    if registry.active_rubric_id() != proposal.parent_rubric_id:
        raise ValueError(
            f"Proposal {proposal_id} is stale because its parent rubric is no longer active"
        )
    proposal.status = "rejected"
    atomic_write_json(PROPOSALS_DIR / f"{proposal_id}.json", proposal.to_dict())
    try:
        registry.close_cycle(
            decision="denied",
            expected_branch="rubric",
            expected_cycle_id=proposal.cycle_id,
        )
    except Exception as exc:
        proposal.status = "proposed"
        _attempt_rollback(
            exc,
            "restore proposed rubric status",
            lambda: atomic_write_json(
                PROPOSALS_DIR / f"{proposal_id}.json",
                proposal.to_dict(),
            ),
        )
        raise
    return proposal


def deny_prompt(prompt_id: str) -> PromptVersion:
    with registry.transaction():
        return _deny_prompt(prompt_id)


def _deny_prompt(prompt_id: str) -> PromptVersion:
    candidate = PromptVersion.from_dict(read_json(CANDIDATES_DIR / f"{prompt_id}.json"))
    if candidate.status != "candidate":
        raise ValueError(f"Prompt {prompt_id} is not in candidate status")
    _require_artifact_cycle("prompt", candidate.cycle_id)
    if registry.active_prompt_id() != candidate.parent_prompt_id:
        raise ValueError(
            f"Prompt {prompt_id} is stale because its parent prompt is no longer active"
        )
    candidate.status = "rejected"
    atomic_write_json(CANDIDATES_DIR / f"{prompt_id}.json", candidate.to_dict())
    try:
        registry.close_cycle(
            decision="denied",
            expected_branch="prompt",
            expected_cycle_id=candidate.cycle_id,
        )
    except Exception as exc:
        candidate.status = "candidate"
        _attempt_rollback(
            exc,
            "restore prompt candidate status",
            lambda: atomic_write_json(
                CANDIDATES_DIR / f"{prompt_id}.json",
                candidate.to_dict(),
            ),
        )
        raise
    return candidate


def update_prompt_candidate(prompt_id: str, text: str) -> PromptVersion:
    with registry.transaction():
        return _update_prompt_candidate(prompt_id, text)


def _update_prompt_candidate(prompt_id: str, text: str) -> PromptVersion:
    candidate = require_current_prompt_candidate(prompt_id)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Prompt text must be a non-empty string")
    candidate.text = text
    atomic_write_json(CANDIDATES_DIR / f"{prompt_id}.json", candidate.to_dict())
    return candidate
