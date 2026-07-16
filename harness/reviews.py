"""Supervisor reviews of individual runs."""

from __future__ import annotations

from dataclasses import replace

from .models import SupervisorReview
from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json

REVIEWS_DIR = EVALS_DIR / "reviews"


def create_review(run_id: str, verdict: str, primary_problem: str,
                   failure_attribution: str | None,
                   reviewer: str = "supervisor", missing_considerations: list[str] | None = None,
                   notes: str = "") -> SupervisorReview:
    if verdict not in ("acceptable", "unacceptable"):
        raise ValueError(f"Invalid verdict: {verdict!r}")
    valid_targets = {"prompt_issue", "rubric_issue", "invalid_run"}
    if verdict == "unacceptable" and failure_attribution not in valid_targets:
        raise ValueError("Unacceptable reviews require a valid change target")
    if verdict == "acceptable":
        failure_attribution = None
    review = SupervisorReview(
        review_id=new_id("rev"), run_id=run_id, verdict=verdict,
        primary_problem=primary_problem, failure_attribution=failure_attribution,
        reviewer=reviewer, created_at=now_iso(),
        missing_considerations=missing_considerations or [], notes=notes,
        status="open",
    )
    atomic_write_json(REVIEWS_DIR / f"{review.review_id}.json", review.to_dict())
    return review


def load_review(review_id: str) -> SupervisorReview:
    return SupervisorReview.from_dict(read_json(REVIEWS_DIR / f"{review_id}.json"))


def list_reviews() -> list[SupervisorReview]:
    if not REVIEWS_DIR.exists():
        return []
    return [SupervisorReview.from_dict(read_json(p)) for p in sorted(REVIEWS_DIR.glob("*.json"))]


def list_open_reviews() -> list[SupervisorReview]:
    return [review for review in list_reviews() if review.status == "open"]


def reviews_for_run(run_id: str) -> list[SupervisorReview]:
    return [r for r in list_reviews() if r.run_id == run_id]


def reviews_by_attribution(attribution: str) -> list[SupervisorReview]:
    return [r for r in list_reviews() if r.failure_attribution == attribution]


def mark_review_used(review_id: str, version_id: str) -> SupervisorReview | None:
    """Persist status=used after a review is applied to a saved prompt/rubric version."""
    path = REVIEWS_DIR / f"{review_id}.json"
    if not path.exists():
        return None
    review = load_review(review_id)
    if review.status == "used" and review.used_by_version_id == version_id:
        return review
    updated = replace(
        review,
        status="used",
        used_by_version_id=version_id,
        used_at=now_iso(),
    )
    atomic_write_json(path, updated.to_dict())
    return updated


def mark_reviews_used(review_ids: list[str], version_id: str) -> None:
    for review_id in review_ids:
        mark_review_used(review_id, version_id)


def delete_review(review_id: str) -> SupervisorReview:
    review = load_review(review_id)
    if review.status == "used":
        raise ValueError(f"Review {review_id!r} was used by {review.used_by_version_id!r}")
    (REVIEWS_DIR / f"{review_id}.json").unlink()
    return review
