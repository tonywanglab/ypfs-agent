"""Conversations, turns, and the response revisions hanging off each turn.

The shape that matters: **a turn owns the query, a run owns an answer.** Asking
something creates one turn and one run. Regenerating that turn after a prompt
revision creates *another run* linked to the same turn at revision_index + 1 —
never another turn. So the transcript shows one query with a stack of responses
under it, the newest live and the rest folded into an accordion, and the model's
replayed history contains that query exactly once.

Links live in chat_run_links rather than as columns on `runs`, so this feature
never alters a table the eval harness owns.
"""

from __future__ import annotations

from .. import dbio
from ..storage import now_iso
from . import ids
from .models import Conversation, Turn

TITLE_WORD_LIMIT = 8

# Chat runs are single-sample by construction (run_case_samples(samples=1)), so
# every answer lives at sample_index 1.
CHAT_SAMPLE_INDEX = 1


def derive_title(query: str, word_limit: int = TITLE_WORD_LIMIT) -> str:
    """First few words of the opening question, for conversation lists."""
    words = query.split()
    if not words:
        return "Untitled"
    snippet = " ".join(words[:word_limit])
    return snippet + "…" if len(words) > word_limit else snippet


# ---- Conversations --------------------------------------------------------

def create(role: str, title: str = "") -> Conversation:
    conversation = Conversation(
        conversation_id=ids.new("conversation"),
        title=title,
        role=role,
        created_at=now_iso(),
    )
    dbio.execute(
        """
        INSERT INTO chat_conversations (conversation_id, title, role, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (conversation.conversation_id, conversation.title, conversation.role,
         conversation.created_at),
    )
    return conversation


def load(conversation_id: str) -> Conversation:
    row = dbio.q1(
        "SELECT * FROM chat_conversations WHERE conversation_id = %s",
        (conversation_id,),
    )
    if row is None:
        raise FileNotFoundError(f"Conversation {conversation_id!r} does not exist")
    return Conversation.from_dict(row)


def set_title(conversation_id: str, title: str) -> None:
    dbio.execute(
        "UPDATE chat_conversations SET title = %s WHERE conversation_id = %s",
        (title, conversation_id),
    )


def list_for_role(role: str) -> list[Conversation]:
    """Conversations visible to `role`.

    Admins see everything, including user threads — curating golden pairs and
    prompt revisions means reading what users actually asked. Users see only
    user-role threads.

    Note there is no per-user isolation: with no user accounts, every `user`
    session sees every user conversation. Fine for a single-operator local tool;
    it would need real identities before this was exposed to several people.
    """
    if role == "admin":
        rows = dbio.q("SELECT * FROM chat_conversations ORDER BY created_at DESC")
    else:
        rows = dbio.q(
            "SELECT * FROM chat_conversations WHERE role = %s ORDER BY created_at DESC",
            (role,),
        )
    return [Conversation.from_dict(row) for row in rows]


def delete(conversation_id: str) -> None:
    """Turns, run links, revisions, and golden pairs cascade. The underlying
    `runs` rows survive — they belong to the harness, not to this feature."""
    deleted = dbio.execute(
        "DELETE FROM chat_conversations WHERE conversation_id = %s",
        (conversation_id,),
    )
    if not deleted:
        raise FileNotFoundError(f"Conversation {conversation_id!r} does not exist")


# ---- Turns ----------------------------------------------------------------

def add_turn(conversation_id: str, query: str, quoted_text: str | None = None,
             quoted_run_id: str | None = None) -> Turn:
    """Append a turn. turn_index is allocated as max+1 inside a transaction;
    UNIQUE (conversation_id, turn_index) turns a race into an error rather than
    two turns silently sharing a position."""
    query = query.strip()
    if not query:
        raise ValueError("query cannot be empty")
    quoted_text = (quoted_text or "").strip() or None

    turn_id = ids.new("turn")
    with dbio.transaction():
        row = dbio.q1(
            """
            INSERT INTO chat_turns (turn_id, conversation_id, turn_index, query,
                                    quoted_text, quoted_run_id, created_at)
            SELECT %s, %s, coalesce(max(turn_index), 0) + 1, %s, %s, %s, %s
              FROM chat_turns WHERE conversation_id = %s
            RETURNING *
            """,
            (turn_id, conversation_id, query, quoted_text, quoted_run_id,
             now_iso(), conversation_id),
        )
    return Turn.from_dict(row)


def load_turn(turn_id: str) -> Turn:
    row = dbio.q1("SELECT * FROM chat_turns WHERE turn_id = %s", (turn_id,))
    if row is None:
        raise FileNotFoundError(f"Turn {turn_id!r} does not exist")
    return Turn.from_dict(row)


def turns_for(conversation_id: str) -> list[Turn]:
    rows = dbio.q(
        "SELECT * FROM chat_turns WHERE conversation_id = %s ORDER BY turn_index",
        (conversation_id,),
    )
    return [Turn.from_dict(row) for row in rows]


def mark_downstream_stale(turn_id: str) -> int:
    """Flag every later turn in the same conversation as stale.

    Regenerating a mid-conversation turn changes the text that later turns were
    answered against. Rather than silently re-running them (which would rewrite
    history the person never asked to change), they are flagged so the UI can
    say so and offer a manual re-run. Returns how many were flagged.
    """
    return dbio.execute(
        """
        UPDATE chat_turns SET stale = true
         WHERE conversation_id = (SELECT conversation_id FROM chat_turns WHERE turn_id = %s)
           AND turn_index > (SELECT turn_index FROM chat_turns WHERE turn_id = %s)
        """,
        (turn_id, turn_id),
    )


# ---- Runs (response revisions) -------------------------------------------

def link_run(run_id: str, turn_id: str, revision_index: int) -> None:
    dbio.execute(
        """
        INSERT INTO chat_run_links (run_id, turn_id, revision_index)
        VALUES (%s, %s, %s)
        ON CONFLICT (run_id) DO UPDATE
            SET turn_id = EXCLUDED.turn_id,
                revision_index = EXCLUDED.revision_index
        """,
        (run_id, turn_id, revision_index),
    )


def next_revision_index(turn_id: str) -> int:
    row = dbio.q1(
        "SELECT coalesce(max(revision_index), 0) + 1 AS next FROM chat_run_links WHERE turn_id = %s",
        (turn_id,),
    )
    return int(row["next"])


def _response_rows(turn_ids: list[str]) -> list[dict]:
    """Every response revision for the given turns, newest revision first.

    One query for the whole transcript rather than per turn — the conversation
    page renders every turn with all of its revisions.
    """
    if not turn_ids:
        return []
    return dbio.q(
        """
        SELECT l.turn_id, l.revision_index, l.run_id,
               r.prompt_id, r.agent_model, r.status, r.created_at,
               s.answer, s.trace
          FROM chat_run_links l
          JOIN runs r ON r.run_id = l.run_id
          LEFT JOIN run_samples s
                 ON s.run_id = l.run_id AND s.sample_index = %s
         WHERE l.turn_id = ANY(%s)
         ORDER BY l.turn_id, l.revision_index DESC
        """,
        (CHAT_SAMPLE_INDEX, turn_ids),
    )


def responses_for(turn_id: str) -> list[dict]:
    """This turn's response revisions, newest first."""
    return _response_rows([turn_id])


def answer_counts(conversation_id: str) -> dict:
    """How many turns exist and how many have an answer — in one query.

    The status endpoint is polled every couple of seconds per open tab, so this
    deliberately avoids calling active_run() per turn (which would be a query
    each) on what is the hottest path in the feature.
    """
    row = dbio.q1(
        """
        SELECT count(*) AS turns,
               count(answered.turn_id) AS answered
          FROM chat_turns t
          LEFT JOIN (
              SELECT DISTINCT l.turn_id
                FROM chat_run_links l
                JOIN run_samples s
                  ON s.run_id = l.run_id AND s.sample_index = %s
          ) answered ON answered.turn_id = t.turn_id
         WHERE t.conversation_id = %s
        """,
        (CHAT_SAMPLE_INDEX, conversation_id),
    )
    return {"turns": int(row["turns"]), "answered": int(row["answered"])}


def active_run(turn_id: str) -> dict | None:
    """The live response for a turn: the highest revision_index that actually
    produced an answer. A crashed run (row present, no sample) is skipped so a
    failed regeneration doesn't blank out a turn that already had an answer."""
    for row in responses_for(turn_id):
        if row["answer"] is not None:
            return row
    return None


# ---- Model-visible text ---------------------------------------------------

def compose_message(turn: Turn) -> str:
    """The text the model sees for a turn.

    A quoted span is rendered as a markdown blockquote above the typed text, so
    "this sentence is wrong" arrives with the sentence attached. One function
    used by both the live run and history replay — the model must never see two
    different renderings of the same turn.
    """
    if not turn.quoted_text:
        return turn.query
    quote = "\n".join(f"> {line}" for line in turn.quoted_text.splitlines())
    return (
        "Regarding this passage from your previous response:\n\n"
        f"{quote}\n\n{turn.query}"
    )


def history_for(conversation_id: str, before_turn_index: int | None = None) -> list[dict]:
    """Replayable message history for a conversation.

    Built from each turn's ACTIVE revision only, so superseded answers never
    re-enter the model's context. `build_trace()` stores the annotated raw
    messages agent.run() returned, which is the same shape it accepts back as
    history — the REPL round-trips them the same way.

    Turns without a usable answer (still running, or crashed) are skipped
    rather than replayed as a dangling user message.
    """
    turns = turns_for(conversation_id)
    if before_turn_index is not None:
        turns = [t for t in turns if t.turn_index < before_turn_index]
    if not turns:
        return []

    by_turn: dict[str, list[dict]] = {}
    for row in _response_rows([t.turn_id for t in turns]):
        by_turn.setdefault(row["turn_id"], []).append(row)

    history: list[dict] = []
    for turn in turns:
        answered = next(
            (row for row in by_turn.get(turn.turn_id, []) if row["answer"] is not None),
            None,
        )
        if answered is None:
            continue
        messages = (answered["trace"] or {}).get("messages") or []
        if messages:
            history.extend(messages)
        else:
            # No trace (e.g. a hand-inserted run): fall back to the plain
            # question/answer pair so continuity survives.
            history.append({"role": "user", "content": compose_message(turn)})
            history.append({"role": "assistant", "content": answered["answer"]})
    return history


# ---- Transcript -----------------------------------------------------------

def timeline(conversation_id: str) -> list[dict]:
    """One time-ordered list of everything the transcript renders: turns (with
    their response revisions) and prompt-revision events.

    Assembled here so the template stays a dumb loop over `kind`.
    """
    turns = turns_for(conversation_id)
    responses: dict[str, list[dict]] = {}
    for row in _response_rows([t.turn_id for t in turns]):
        responses.setdefault(row["turn_id"], []).append(row)

    events: list[dict] = []
    for turn in turns:
        revisions = responses.get(turn.turn_id, [])
        active = next((r for r in revisions if r["answer"] is not None), None)
        superseded = [r for r in revisions if active is None or r["run_id"] != active["run_id"]]
        events.append({
            "kind": "turn",
            "sort_key": (turn.created_at, turn.turn_index),
            "turn": turn,
            "active": active,
            "superseded": superseded,
        })

    revision_rows = dbio.q(
        """
        SELECT * FROM chat_prompt_revisions
         WHERE conversation_id = %s AND status = 'accepted'
         ORDER BY created_at
        """,
        (conversation_id,),
    )
    for row in revision_rows:
        events.append({
            "kind": "prompt_revision",
            # Sorts after the turn it came from: same created_at ties break on
            # the turn's index, and a revision always follows its own turn.
            "sort_key": (row["created_at"], 10**9),
            "revision": row,
        })

    events.sort(key=lambda event: event["sort_key"])
    return events


def pending_revisions(conversation_id: str) -> list[dict]:
    """Proposals awaiting an admin decision, oldest first."""
    return dbio.q(
        """
        SELECT * FROM chat_prompt_revisions
         WHERE conversation_id = %s AND status = 'proposed'
         ORDER BY created_at
        """,
        (conversation_id,),
    )
