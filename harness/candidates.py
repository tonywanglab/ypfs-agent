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
import re

from . import llm, registry, reviews
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


def propose_rubric(review_ids: list[str], model: str, *, opened_by: str = "supervisor") -> Rubric:
    """Generate a rubric proposal from supervisor reviews. Locks the rubric
    branch for this cycle; raises CycleLockedError if the prompt branch is
    already open."""
    registry.lock_cycle("rubric", opened_by=opened_by)
    parent = load_rubric(registry.active_rubric_id())
    payload = {
        "parent_rubric": parent.to_dict(),
        "supervisor_feedback": _review_context(review_ids),
    }
    parsed = llm.chat_json(RUBRIC_PROPOSAL_SYSTEM, json.dumps(payload, indent=2, default=str), model)
    version = _next_rubric_version()
    criteria = [
        RubricCriterion(
            id=c["id"],
            description=c["description"],
            check_type=c.get("check_type", "llm"),
            weight=float(c.get("weight", 1.0)),
            deterministic_check=c.get("deterministic_check"),
        )
        for c in parsed.get("criteria", [])
    ]
    proposal = Rubric(
        rubric_id=f"rubric_v{version}_prop_{new_id('')}",
        version=version,
        status="proposed",
        criteria=criteria,
        created_at=now_iso(),
        parent_rubric_id=parent.rubric_id,
        rationale=parsed.get("rationale", ""),
        derived_from_review_ids=review_ids,
    )
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(PROPOSALS_DIR / f"{proposal.rubric_id}.json", proposal.to_dict())
    return proposal


def propose_prompt(review_ids: list[str], model: str, *, opened_by: str = "supervisor") -> PromptVersion:
    """Generate a prompt candidate from agent_failure reviews."""
    registry.lock_cycle("prompt", opened_by=opened_by)
    parent = load_prompt(registry.active_prompt_id())
    payload = {
        "parent_prompt": parent.to_dict(),
        "supervisor_feedback": _review_context(review_ids),
    }
    parsed = llm.chat_json(PROMPT_PROPOSAL_SYSTEM, json.dumps(payload, indent=2, default=str), model)
    version = _next_prompt_version()
    candidate = PromptVersion(
        prompt_id=f"prompt_v{version}_{new_id('')}",
        version=version,
        status="candidate",
        text=parsed.get("text", parent.text),
        created_at=now_iso(),
        parent_prompt_id=parent.prompt_id,
        rationale=parsed.get("rationale", ""),
        derived_from_review_ids=review_ids,
    )
    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(CANDIDATES_DIR / f"{candidate.prompt_id}.json", candidate.to_dict())
    return candidate


def _parse_criteria_json(text: str) -> list[RubricCriterion]:
    data = json.loads(text)
    return [
        RubricCriterion(
            id=c["id"],
            description=c["description"],
            check_type=c.get("check_type", "llm"),
            weight=float(c.get("weight", 1.0)),
            deterministic_check=c.get("deterministic_check"),
        )
        for c in data
    ]


def approve_rubric(proposal_id: str, criteria_json: str | None = None) -> Rubric:
    """Freeze a proposal as the new active rubric version."""
    proposal = Rubric.from_dict(read_json(PROPOSALS_DIR / f"{proposal_id}.json"))
    if proposal.status != "proposed":
        raise ValueError(f"Proposal {proposal_id} is not in proposed status")

    criteria = _parse_criteria_json(criteria_json) if criteria_json else proposal.criteria
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
    )
    atomic_write_json(RUBRICS_DIR / f"{frozen.rubric_id}.json", frozen.to_dict())

    proposal.status = "rejected"  # proposal artifact kept but marked consumed
    atomic_write_json(PROPOSALS_DIR / f"{proposal_id}.json", proposal.to_dict())

    registry.set_active_rubric(frozen.rubric_id)
    registry.close_cycle(decision="approved")
    return frozen


def deny_rubric(proposal_id: str) -> Rubric:
    proposal = Rubric.from_dict(read_json(PROPOSALS_DIR / f"{proposal_id}.json"))
    proposal.status = "rejected"
    atomic_write_json(PROPOSALS_DIR / f"{proposal_id}.json", proposal.to_dict())
    registry.close_cycle(decision="denied")
    return proposal


def deny_prompt(prompt_id: str) -> PromptVersion:
    candidate = PromptVersion.from_dict(read_json(CANDIDATES_DIR / f"{prompt_id}.json"))
    candidate.status = "rejected"
    atomic_write_json(CANDIDATES_DIR / f"{prompt_id}.json", candidate.to_dict())
    registry.close_cycle(decision="denied")
    return candidate
