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
from .runner import PROMOTIONS_DIR, promotion_has_blocked_candidate_run, save_promotion
from .storage import (
    EVALS_DIR,
    REPO_ROOT,
    atomic_write_json,
    atomic_write_text,
    now_iso,
    read_json,
)

PROMPTS_DIR = EVALS_DIR / "prompts"
CANDIDATES_DIR = PROMPTS_DIR / "candidates"
ARCHIVE_DIR = PROMPTS_DIR / "archive"
SYSTEM_PROMPT_PATH = REPO_ROOT / "agent" / "system_prompt.md"


def _require_pending_promotion(promotion, candidate: PromptVersion | None = None) -> None:
    if promotion.status != "pending":
        raise ValueError(f"Promotion {promotion.promotion_id} is not pending")
    if promotion.cycle_id is None:
        raise ValueError("Promotion is missing its review cycle identity")
    registry.require_cycle("prompt", cycle_id=promotion.cycle_id)
    if registry.active_prompt_id() != promotion.incumbent_prompt_id:
        raise ValueError("Promotion incumbent is no longer the active prompt")
    if candidate is not None:
        if candidate.status != "candidate":
            raise ValueError(f"Prompt {candidate.prompt_id} is not in candidate status")
        if candidate.parent_prompt_id != promotion.incumbent_prompt_id:
            raise ValueError("Prompt candidate does not descend from the promotion incumbent")
        if candidate.cycle_id != promotion.cycle_id:
            raise ValueError("Prompt candidate belongs to a different review cycle")


def _rollback(cause: Exception, description: str, action) -> None:
    try:
        action()
    except Exception as rollback_error:
        cause.add_note(f"Failed to {description}: {rollback_error}")


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
    _require_pending_promotion(promotion, candidate)

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = ARCHIVE_DIR / f"{incumbent.prompt_id}.json"
    active_path = PROMPTS_DIR / f"{candidate.prompt_id}.json"
    candidate_path = CANDIDATES_DIR / f"{candidate_prompt_id}.json"
    if archive_path.exists():
        raise ValueError(f"Archive for {incumbent.prompt_id} already exists")
    if active_path.exists():
        raise ValueError(f"Active prompt {candidate.prompt_id} already exists")

    system_existed = SYSTEM_PROMPT_PATH.exists()
    system_was_file = SYSTEM_PROMPT_PATH.is_file()
    system_text = SYSTEM_PROMPT_PATH.read_text() if system_was_file else None
    original_candidate = candidate.to_dict()
    original_promotion = promotion.to_dict()

    archived = PromptVersion(
        prompt_id=incumbent.prompt_id,
        version=incumbent.version,
        status="archived",
        text=incumbent.text,
        created_at=now_iso(),
        parent_prompt_id=incumbent.parent_prompt_id,
        rationale=f"Archived on promotion of {candidate_prompt_id}",
        derived_from_review_ids=incumbent.derived_from_review_ids,
        cycle_id=incumbent.cycle_id,
    )

    active = PromptVersion(
        prompt_id=candidate.prompt_id,
        version=candidate.version,
        status="active",
        text=candidate.text,
        created_at=now_iso(),
        parent_prompt_id=candidate.parent_prompt_id,
        rationale=candidate.rationale,
        derived_from_review_ids=candidate.derived_from_review_ids,
        cycle_id=candidate.cycle_id,
    )
    try:
        atomic_write_json(archive_path, archived.to_dict())
        atomic_write_json(active_path, active.to_dict())
        atomic_write_text(SYSTEM_PROMPT_PATH, active.text)

        candidate.status = "archived"
        atomic_write_json(candidate_path, candidate.to_dict())

        promotion.status = "approved"
        promotion.decided_at = now_iso()
        promotion.rationale = f"Promoted {candidate_prompt_id} over {incumbent.prompt_id}"
        save_promotion(promotion)

        registry.activate_prompt_and_close(active.prompt_id, cycle_id=promotion.cycle_id)
        return active
    except Exception as exc:
        _rollback(
            exc,
            "restore prompt candidate",
            lambda: atomic_write_json(candidate_path, original_candidate),
        )
        _rollback(
            exc,
            "restore promotion manifest",
            lambda: atomic_write_json(
                PROMOTIONS_DIR / promotion_id / "manifest.json",
                original_promotion,
            ),
        )
        _rollback(exc, "remove incomplete active prompt", lambda: active_path.unlink(missing_ok=True))
        _rollback(exc, "remove incomplete archive", lambda: archive_path.unlink(missing_ok=True))
        if system_was_file:
            _rollback(
                exc,
                "restore system prompt",
                lambda: atomic_write_text(SYSTEM_PROMPT_PATH, system_text),
            )
        elif not system_existed:
            _rollback(
                exc,
                "remove incomplete system prompt",
                lambda: SYSTEM_PROMPT_PATH.unlink(missing_ok=True),
            )
        raise


def deny_promotion(promotion_id: str, rationale: str = "") -> None:
    from .runner import load_promotion

    promotion = load_promotion(promotion_id)
    _require_pending_promotion(promotion)
    original = promotion.to_dict()
    promotion.status = "denied"
    promotion.decided_at = now_iso()
    promotion.rationale = rationale or "Denied by supervisor"
    save_promotion(promotion)
    try:
        registry.close_cycle(
            decision="denied",
            expected_branch="prompt",
            expected_cycle_id=promotion.cycle_id,
        )
    except Exception as exc:
        _rollback(
            exc,
            "restore pending promotion",
            lambda: atomic_write_json(
                PROMOTIONS_DIR / promotion_id / "manifest.json",
                original,
            ),
        )
        raise
