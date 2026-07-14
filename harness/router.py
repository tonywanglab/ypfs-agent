"""Route supervisor reviews into the rubric or prompt update branch.

Each review cycle may approve exactly one artifact type. If the other branch
is already locked, the review is queued for the next cycle rather than
rejected.
"""

from __future__ import annotations

from . import registry
from .models import SupervisorReview

RUBRIC_ATTRIBUTIONS = frozenset({"rubric_gap", "judge_failure"})
PROMPT_ATTRIBUTIONS = frozenset({"agent_failure"})


def branch_for_attribution(attribution: str) -> str | None:
    """Map a failure_attribution to the update branch it implies, if any."""
    if attribution in RUBRIC_ATTRIBUTIONS:
        return "rubric"
    if attribution in PROMPT_ATTRIBUTIONS:
        return "prompt"
    return None


def route_review(review: SupervisorReview) -> dict:
    """After a supervisor review is saved, enqueue it if the implied branch
    conflicts with the currently locked branch. Returns a small status dict
    for the UI."""
    if review.verdict == "acceptable":
        return {"action": "none", "branch": None, "queued": False}

    branch = branch_for_attribution(review.failure_attribution)
    if branch is None:
        return {"action": "manual", "branch": None, "queued": False}

    locked = registry.locked_branch()
    if locked is not None and locked != branch:
        registry.enqueue(branch, review.review_id)
        return {"action": "queued", "branch": branch, "queued": True}

    return {"action": "ready", "branch": branch, "queued": False}
