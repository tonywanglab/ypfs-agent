"""Supervisor reviews of individual runs.

This is the ground signal that routes into exactly one update branch per
cycle (see harness.registry). Reviews are plain files; there is no
"consumed" tracking — the caller (the web UI) explicitly selects which
review_ids feed a given rubric proposal or prompt candidate.
"""

from __future__ import annotations

from .models import SupervisorReview
from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json

REVIEWS_DIR = EVALS_DIR / "reviews"


def create_review(run_id: str, verdict: str, primary_problem: str, failure_attribution: str,
                   reviewer: str = "supervisor", missing_considerations: list[str] | None = None,
                   notes: str = "") -> SupervisorReview:
    review = SupervisorReview(
        review_id=new_id("rev"), run_id=run_id, verdict=verdict,
        primary_problem=primary_problem, failure_attribution=failure_attribution,
        reviewer=reviewer, created_at=now_iso(),
        missing_considerations=missing_considerations or [], notes=notes,
    )
    atomic_write_json(REVIEWS_DIR / f"{review.review_id}.json", review.to_dict())
    return review


def load_review(review_id: str) -> SupervisorReview:
    return SupervisorReview.from_dict(read_json(REVIEWS_DIR / f"{review_id}.json"))


def list_reviews() -> list[SupervisorReview]:
    if not REVIEWS_DIR.exists():
        return []
    return [SupervisorReview.from_dict(read_json(p)) for p in sorted(REVIEWS_DIR.glob("*.json"))]


def reviews_for_run(run_id: str) -> list[SupervisorReview]:
    return [r for r in list_reviews() if r.run_id == run_id]


def reviews_by_attribution(attribution: str) -> list[SupervisorReview]:
    return [r for r in list_reviews() if r.failure_attribution == attribution]
