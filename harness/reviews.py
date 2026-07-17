"""Supervisor reviews of individual runs (Postgres-backed CRUD)."""

from __future__ import annotations

from . import dbio
from .models import SupervisorReview
from .storage import new_id, now_iso


def _from_row(row: dict) -> SupervisorReview:
    return SupervisorReview.from_dict({
        **row,
        "missing_considerations": row["missing_considerations"] or [],
    })


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
    dbio.execute(
        """
        INSERT INTO reviews (review_id, run_id, verdict, primary_problem,
                             failure_attribution, reviewer, missing_considerations,
                             notes, status, used_by_version_id, used_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (review.review_id, review.run_id, review.verdict, review.primary_problem,
         review.failure_attribution, review.reviewer,
         dbio.jsonb(review.missing_considerations), review.notes, review.status,
         review.used_by_version_id, review.used_at, review.created_at),
    )
    return review


def load_review(review_id: str) -> SupervisorReview:
    row = dbio.q1("SELECT * FROM reviews WHERE review_id = %s", (review_id,))
    if row is None:
        raise FileNotFoundError(f"Review {review_id!r} does not exist")
    return _from_row(row)


def list_reviews() -> list[SupervisorReview]:
    rows = dbio.q("SELECT * FROM reviews ORDER BY created_at, review_id")
    return [_from_row(row) for row in rows]


def list_open_reviews() -> list[SupervisorReview]:
    rows = dbio.q(
        "SELECT * FROM reviews WHERE status = 'open' ORDER BY created_at, review_id"
    )
    return [_from_row(row) for row in rows]


def reviews_for_run(run_id: str) -> list[SupervisorReview]:
    rows = dbio.q(
        "SELECT * FROM reviews WHERE run_id = %s ORDER BY created_at, review_id",
        (run_id,),
    )
    return [_from_row(row) for row in rows]


def reviews_by_attribution(attribution: str) -> list[SupervisorReview]:
    rows = dbio.q(
        "SELECT * FROM reviews WHERE failure_attribution = %s"
        " ORDER BY created_at, review_id",
        (attribution,),
    )
    return [_from_row(row) for row in rows]


def mark_review_used(review_id: str, version_id: str) -> SupervisorReview | None:
    """Persist status=used after a review is applied to a saved prompt/rubric version."""
    dbio.execute(
        """
        UPDATE reviews SET status = 'used', used_by_version_id = %s, used_at = %s
        WHERE review_id = %s
          AND NOT (status = 'used' AND used_by_version_id = %s)
        """,
        (version_id, now_iso(), review_id, version_id),
    )
    try:
        return load_review(review_id)
    except FileNotFoundError:
        return None


def mark_reviews_used(review_ids: list[str], version_id: str) -> None:
    for review_id in review_ids:
        mark_review_used(review_id, version_id)


def delete_review(review_id: str) -> SupervisorReview:
    review = load_review(review_id)
    if review.status == "used":
        raise ValueError(f"Review {review_id!r} was used by {review.used_by_version_id!r}")
    dbio.execute("DELETE FROM version_reviews WHERE review_id = %s", (review_id,))
    dbio.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
    return review
