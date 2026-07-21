"""Selection-based supervisor feedback on a run's answer (Postgres-backed CRUD)."""

from __future__ import annotations

from . import dbio
from .models import Feedback
from .storage import new_id, now_iso


def _from_row(row: dict) -> Feedback:
    return Feedback.from_dict(row)


def create_feedback(run_id: str, sample_index: int, selected_text: str,
                     comment: str) -> Feedback:
    selected_text = selected_text.strip()
    comment = comment.strip()
    if not selected_text:
        raise ValueError("selected_text cannot be empty")
    if not comment:
        raise ValueError("comment cannot be empty")
    feedback = Feedback(
        feedback_id=new_id("fb"), run_id=run_id, sample_index=sample_index,
        selected_text=selected_text, comment=comment, created_at=now_iso(),
    )
    dbio.execute(
        """
        INSERT INTO feedback (feedback_id, run_id, sample_index, selected_text,
                              comment, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (feedback.feedback_id, feedback.run_id, feedback.sample_index,
         feedback.selected_text, feedback.comment, feedback.created_at),
    )
    return feedback


def load_feedback(feedback_id: str) -> Feedback:
    row = dbio.q1("SELECT * FROM feedback WHERE feedback_id = %s", (feedback_id,))
    if row is None:
        raise FileNotFoundError(f"Feedback {feedback_id!r} does not exist")
    return _from_row(row)


def feedback_for_run(run_id: str) -> list[Feedback]:
    rows = dbio.q(
        "SELECT * FROM feedback WHERE run_id = %s ORDER BY created_at, feedback_id",
        (run_id,),
    )
    return [_from_row(row) for row in rows]


def delete_feedback(feedback_id: str) -> Feedback:
    feedback = load_feedback(feedback_id)
    dbio.execute("DELETE FROM feedback WHERE feedback_id = %s", (feedback_id,))
    return feedback
