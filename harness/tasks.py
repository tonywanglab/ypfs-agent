"""Postgres-backed task queue.

One `tasks` row per unit of background work — experiment runs and prompt
draft generations share the table, distinguished by `kind`.
The row is the single source of truth end-to-end: the DB row, the
/tasks/<id>/status JSON, and the frontend's polling state all carry the same
shape (see task_payload()).

Claiming is a single atomic UPDATE ... FOR UPDATE SKIP LOCKED statement, so
it is safe on autocommit connections and behind a transaction-mode pooler,
and N workers never double-claim. Workers bump heartbeat_at while executing;
requeue_stale() returns abandoned claims to the queue (or fails them past
MAX_ATTEMPTS).
"""

from __future__ import annotations

import re
from typing import Any

from . import dbio
from .storage import new_id

KIND_EXPERIMENT = "experiment"
KIND_PROMPT_DRAFT = "prompt_draft"
# Chat UI (harness/chat/): one turn of a conversation, and re-answering a turn
# after its system prompt was revised. Named here because enqueue() validates
# against KINDS; their executors are registered by harness/chat/runs.py.
KIND_CHAT_TURN = "chat_turn"
KIND_CHAT_REGENERATE = "chat_regenerate"
KINDS = (KIND_EXPERIMENT, KIND_PROMPT_DRAFT, KIND_CHAT_TURN, KIND_CHAT_REGENERATE)

# In-flight from the UI's perspective: keep polling.
ACTIVE_STATUSES = ("queued", "running")

HEARTBEAT_TIMEOUT_S = 120
MAX_ATTEMPTS = 3

_TASK_ID_RE = re.compile(r"^task_[0-9a-f]{12}$")


def new_task_id() -> str:
    return new_id("task")


def is_task_id(task_id: str) -> bool:
    return bool(_TASK_ID_RE.fullmatch(task_id or ""))


def task_payload(row: dict) -> dict:
    """The one task datashape: DB row -> JSON-safe dict (API + frontend)."""
    return {
        "task_id": row["task_id"],
        "kind": row["kind"],
        "status": row["status"],
        "payload": row["payload"] or {},
        "progress": row["progress"] or {},
        "result": row["result"],
        "run_id": row["run_id"],
        "error": row["error"],
        "attempts": row["attempts"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "finished_at": row["finished_at"].isoformat() if row["finished_at"] else None,
    }


def enqueue(kind: str, payload: dict, task_id: str | None = None) -> dict:
    if kind not in KINDS:
        raise ValueError(f"Unknown task kind: {kind!r}")
    if task_id is None:
        task_id = new_task_id()
    elif not is_task_id(task_id):
        raise ValueError(f"Invalid task id: {task_id!r}")
    row = dbio.q1(
        """
        INSERT INTO tasks (task_id, kind, status, payload)
        VALUES (%s, %s, 'queued', %s)
        RETURNING *
        """,
        (task_id, kind, dbio.jsonb(payload)),
    )
    return task_payload(row)


def claim(worker_name: str) -> dict | None:
    """Atomically claim the oldest queued task, or None when the queue is empty."""
    row = dbio.q1(
        """
        UPDATE tasks
           SET status = 'running', claimed_by = %s, claimed_at = now(),
               heartbeat_at = now(), attempts = attempts + 1
         WHERE task_id = (
                   SELECT task_id FROM tasks
                    WHERE status = 'queued'
                    ORDER BY created_at
                    LIMIT 1
                      FOR UPDATE SKIP LOCKED
               )
        RETURNING *
        """,
        (worker_name,),
    )
    return task_payload(row) if row else None


def heartbeat(task_id: str) -> None:
    dbio.execute(
        "UPDATE tasks SET heartbeat_at = now() WHERE task_id = %s AND status = 'running'",
        (task_id,),
    )


def set_progress(task_id: str, **fields: Any) -> None:
    """Merge fields into the progress jsonb and refresh the heartbeat."""
    dbio.execute(
        """
        UPDATE tasks
           SET progress = progress || %s, heartbeat_at = now()
         WHERE task_id = %s
        """,
        (dbio.jsonb(fields), task_id),
    )


def set_run(task_id: str, run_id: str) -> None:
    dbio.execute(
        "UPDATE tasks SET run_id = %s WHERE task_id = %s AND run_id IS DISTINCT FROM %s",
        (run_id, task_id, run_id),
    )


def finish(task_id: str, result: dict | None = None) -> None:
    dbio.execute(
        """
        UPDATE tasks SET status = 'finished', result = %s, error = NULL,
                         finished_at = now()
         WHERE task_id = %s
        """,
        (dbio.jsonb(result) if result is not None else None, task_id),
    )


def fail(task_id: str, error: str) -> None:
    dbio.execute(
        """
        UPDATE tasks SET status = 'failed', error = %s, finished_at = now()
         WHERE task_id = %s
        """,
        (error, task_id),
    )


def load(task_id: str) -> dict:
    row = dbio.q1("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    if row is None:
        raise FileNotFoundError(f"Task {task_id!r} does not exist")
    return task_payload(row)


def list_active() -> list[dict]:
    rows = dbio.q(
        "SELECT * FROM tasks WHERE status = ANY(%s) ORDER BY created_at",
        (list(ACTIVE_STATUSES),),
    )
    return [task_payload(row) for row in rows]


def list_recent(limit: int = 20) -> list[dict]:
    rows = dbio.q(
        "SELECT * FROM tasks ORDER BY created_at DESC LIMIT %s",
        (limit,),
    )
    return [task_payload(row) for row in rows]


def requeue_stale(timeout_s: int = HEARTBEAT_TIMEOUT_S,
                  max_attempts: int = MAX_ATTEMPTS) -> int:
    """Return abandoned running tasks to the queue; fail them past max_attempts.

    A task whose worker died stops heartbeating; after timeout_s it is either
    requeued (attempts < max_attempts — the claim will re-increment attempts)
    or failed for good.
    """
    return dbio.execute(
        """
        UPDATE tasks
           SET status = CASE WHEN attempts >= %(max)s THEN 'failed' ELSE 'queued' END,
               error  = CASE WHEN attempts >= %(max)s
                             THEN 'worker heartbeat timeout after ' || %(max)s || ' attempts'
                             ELSE error END,
               finished_at = CASE WHEN attempts >= %(max)s THEN now() ELSE finished_at END,
               claimed_by = NULL
         WHERE status = 'running'
           AND heartbeat_at < now() - make_interval(secs => %(timeout)s)
        """,
        {"max": max_attempts, "timeout": timeout_s},
    )
