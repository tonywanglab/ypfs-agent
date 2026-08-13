"""Golden query/response pairs — an admin-curated reference set.

Marking a response stores a **snapshot** of the query and the answer, not a
pointer to them. That is the whole point: this is a labeled dataset for a future
LLM-as-judge, so regenerating the turn it came from, revising the prompt, or
deleting the conversation must never silently change what a saved pair says.
`run_id` is kept anyway (UNIQUE) so marking is idempotent per response revision
and the UI can link back to where the pair came from.

No scoring, no judging, no rubric here. Just capture and retrieval.
"""

from __future__ import annotations

from .. import dbio
from ..storage import now_iso
from . import conversations, ids
from .models import GoldenPair


def _from_row(row: dict) -> GoldenPair:
    return GoldenPair.from_dict(row)


def mark(turn_id: str, run_id: str, note: str = "") -> GoldenPair:
    """Snapshot one turn's response as a golden pair.

    The stored `query` is the composed message the model actually received
    (quoted span included), not just the typed text — a judge has to see the
    same input the answer was produced from.
    """
    turn = conversations.load_turn(turn_id)
    response = next(
        (r for r in conversations.responses_for(turn_id) if r["run_id"] == run_id),
        None,
    )
    if response is None:
        raise FileNotFoundError(f"Run {run_id!r} is not a response to turn {turn_id!r}")
    if response["answer"] is None:
        raise ValueError("Cannot mark a response that has no answer yet")

    pair = GoldenPair(
        golden_id=ids.new("golden"),
        conversation_id=turn.conversation_id,
        turn_id=turn_id,
        run_id=run_id,
        query=conversations.compose_message(turn),
        answer=response["answer"],
        prompt_id=response["prompt_id"],
        agent_model=response["agent_model"],
        note=(note or "").strip(),
        created_at=now_iso(),
    )
    dbio.execute(
        """
        INSERT INTO chat_golden_pairs
            (golden_id, conversation_id, turn_id, run_id, query, answer,
             prompt_id, agent_model, note, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (run_id) DO NOTHING
        """,
        (pair.golden_id, pair.conversation_id, pair.turn_id, pair.run_id,
         pair.query, pair.answer, pair.prompt_id, pair.agent_model,
         pair.note, pair.created_at),
    )
    # ON CONFLICT means an already-marked response returns the existing row
    # rather than erroring — the star is a toggle, not a transaction.
    return for_run(run_id) or pair


def unmark(run_id: str) -> GoldenPair | None:
    """Remove the pair for a response. Returns what was removed, or None."""
    existing = for_run(run_id)
    if existing is None:
        return None
    dbio.execute("DELETE FROM chat_golden_pairs WHERE run_id = %s", (run_id,))
    return existing


def delete(golden_id: str) -> GoldenPair:
    pair = load(golden_id)
    dbio.execute("DELETE FROM chat_golden_pairs WHERE golden_id = %s", (golden_id,))
    return pair


def load(golden_id: str) -> GoldenPair:
    row = dbio.q1(
        "SELECT * FROM chat_golden_pairs WHERE golden_id = %s", (golden_id,)
    )
    if row is None:
        raise FileNotFoundError(f"Golden pair {golden_id!r} does not exist")
    return _from_row(row)


def for_run(run_id: str) -> GoldenPair | None:
    row = dbio.q1("SELECT * FROM chat_golden_pairs WHERE run_id = %s", (run_id,))
    return _from_row(row) if row else None


def marked_run_ids(run_ids: list[str]) -> set[str]:
    """Which of these responses are already marked — one query for a whole
    transcript, so the star renders in the right state without N lookups."""
    if not run_ids:
        return set()
    rows = dbio.q(
        "SELECT run_id FROM chat_golden_pairs WHERE run_id = ANY(%s)", (run_ids,)
    )
    return {row["run_id"] for row in rows}


def list_pairs(prompt_id: str = "") -> list[GoldenPair]:
    """Newest first, optionally filtered to one prompt version."""
    if prompt_id:
        rows = dbio.q(
            "SELECT * FROM chat_golden_pairs WHERE prompt_id = %s "
            "ORDER BY created_at DESC, golden_id",
            (prompt_id,),
        )
    else:
        rows = dbio.q(
            "SELECT * FROM chat_golden_pairs ORDER BY created_at DESC, golden_id"
        )
    return [_from_row(row) for row in rows]


def prompt_ids_with_pairs() -> list[str]:
    """Prompt versions that have at least one pair, for the filter control."""
    rows = dbio.q(
        "SELECT DISTINCT prompt_id FROM chat_golden_pairs ORDER BY prompt_id"
    )
    return [row["prompt_id"] for row in rows]
