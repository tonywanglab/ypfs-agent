"""Manual prompt promotion after supervisor A/B review.

Promotion atomically:
  1. archives the incumbent prompt under evals/prompts/archive/
  2. writes the approved candidate text to agent/system_prompt.md
  3. saves the candidate as the new active prompt under evals/prompts/
  4. updates registry.active_prompt_id

Blocked if any candidate run in the promotion hit a deterministic hard failure.
"""

from __future__ import annotations

from . import registry
from .candidates import load_prompt
from .models import PromptVersion
from .runner import promotion_has_blocked_candidate_run, save_promotion
from .storage import EVALS_DIR, REPO_ROOT, atomic_write_json, now_iso, read_json

PROMPTS_DIR = EVALS_DIR / "prompts"
CANDIDATES_DIR = PROMPTS_DIR / "candidates"
ARCHIVE_DIR = PROMPTS_DIR / "archive"
SYSTEM_PROMPT_PATH = REPO_ROOT / "agent" / "system_prompt.md"


def promote_prompt(promotion_id: str, candidate_prompt_id: str) -> PromptVersion:
    from .runner import load_promotion

    if promotion_has_blocked_candidate_run(promotion_id):
        raise ValueError(
            "Cannot promote: at least one candidate run has a deterministic hard failure."
        )

    promotion = load_promotion(promotion_id)
    if promotion.candidate_prompt_id != candidate_prompt_id:
        raise ValueError("candidate_prompt_id does not match this promotion")

    incumbent = load_prompt(promotion.incumbent_prompt_id)
    candidate = PromptVersion.from_dict(read_json(CANDIDATES_DIR / f"{candidate_prompt_id}.json"))

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archived = PromptVersion(
        prompt_id=incumbent.prompt_id,
        version=incumbent.version,
        status="archived",
        text=incumbent.text,
        created_at=now_iso(),
        parent_prompt_id=incumbent.parent_prompt_id,
        rationale=f"Archived on promotion of {candidate_prompt_id}",
        derived_from_review_ids=incumbent.derived_from_review_ids,
    )
    atomic_write_json(ARCHIVE_DIR / f"{archived.prompt_id}.json", archived.to_dict())

    active = PromptVersion(
        prompt_id=candidate.prompt_id,
        version=candidate.version,
        status="active",
        text=candidate.text,
        created_at=now_iso(),
        parent_prompt_id=candidate.parent_prompt_id,
        rationale=candidate.rationale,
        derived_from_review_ids=candidate.derived_from_review_ids,
    )
    atomic_write_json(PROMPTS_DIR / f"{active.prompt_id}.json", active.to_dict())
    SYSTEM_PROMPT_PATH.write_text(active.text)

    candidate.status = "archived"
    atomic_write_json(CANDIDATES_DIR / f"{candidate_prompt_id}.json", candidate.to_dict())

    registry.set_active_prompt(active.prompt_id)
    registry.close_cycle(decision="approved")

    promotion.status = "approved"
    promotion.decided_at = now_iso()
    promotion.rationale = f"Promoted {candidate_prompt_id} over {incumbent.prompt_id}"
    save_promotion(promotion)

    return active


def deny_promotion(promotion_id: str, rationale: str = "") -> None:
    from .runner import load_promotion

    promotion = load_promotion(promotion_id)
    promotion.status = "denied"
    promotion.decided_at = now_iso()
    promotion.rationale = rationale or "Denied by supervisor"
    save_promotion(promotion)
    registry.close_cycle(decision="denied")
