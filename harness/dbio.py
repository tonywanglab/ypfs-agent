"""Postgres access layer for the harness.

All harness SQL goes through these helpers, which run on the per-thread
connection from db.get_thread_conn() (autocommit, pooler-safe). Queries are
parameterized-only by construction: every helper takes (sql, params) and no
harness module ever interpolates values into SQL text.

Also home of the strict record-id validators: each id family has an anchored
regex, and web routes reject anything that doesn't match before it reaches a
query.
"""

from __future__ import annotations

import re
import sys
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import db  # repo-root connection seam


def _conn():
    return db.get_thread_conn()


def jsonb(value: Any):
    """Wrap a Python object for insertion into a jsonb column."""
    from psycopg.types.json import Jsonb
    return Jsonb(value)


# True while this thread is inside an explicit transaction() block. Retrying one
# statement of a multi-statement transaction on a new connection would silently
# drop the statements before it, so the retry below refuses to do that.
_IN_TRANSACTION = threading.local()


def _connection_lost(exc: Exception) -> bool:
    """Is this a dead connection rather than a bad query?

    A hosted Postgres closes idle connections, and psycopg reports that as
    OperationalError/InterfaceError on the next use. A syntax error or a
    constraint violation is a different class entirely and must propagate.
    """
    import psycopg
    return isinstance(exc, (psycopg.OperationalError, psycopg.InterfaceError))


def _run(fn):
    """Execute fn(conn), retrying once on a fresh connection if the old one died.

    Without this, the first request after the database drops an idle connection
    fails — and for the web UI that is a 500 on a page the operator was just
    looking at. The worker loop has its own recovery; this covers everyone else.
    """
    try:
        return fn(_conn())
    except Exception as exc:
        if getattr(_IN_TRANSACTION, "active", False) or not _connection_lost(exc):
            raise
        reset_conn()
        return fn(_conn())


def q(sql: str, params: tuple | dict = ()) -> list[dict]:
    """Run a SELECT and return all rows as dicts."""
    from psycopg.rows import dict_row

    def go(conn):
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    return _run(go)


def q1(sql: str, params: tuple | dict = ()) -> dict | None:
    """Run a SELECT (or RETURNING statement) and return the first row or None."""
    rows = q(sql, params)
    return rows[0] if rows else None


def execute(sql: str, params: tuple | dict = ()) -> int:
    """Run a statement; returns the affected row count."""
    def go(conn):
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount

    return _run(go)


def reset_conn() -> None:
    """Discard this thread's connection so the next call opens a fresh one.

    A dropped network connection doesn't always leave psycopg's handle in a
    state it reports as closed — it can be left holding an unconsumed result, and
    then every later query on it fails with "another command is already in
    progress" forever. A caller that loops (the queue worker) has to throw the
    handle away on error, or it spins on a connection that can never recover.

    Safe to call when there is no connection, and never raises.
    """
    conn = getattr(db._THREAD_LOCAL, "conn", None)
    db._THREAD_LOCAL.conn = None
    if conn is None:
        return
    try:
        conn.close()
    except Exception:
        pass  # already dead; we only wanted to release the socket


@contextmanager
def transaction():
    """Explicit transaction block for multi-statement writes.

    Usage: `with dbio.transaction():` — psycopg issues BEGIN/COMMIT around the
    block even on an autocommit connection.

    Also marks the thread as in-transaction so _run() won't transparently retry
    a single statement on a new connection and lose the ones before it. A
    connection that dies mid-transaction is a failure the caller must see.
    """
    was_active = getattr(_IN_TRANSACTION, "active", False)
    _IN_TRANSACTION.active = True
    try:
        with _conn().transaction() as tx:
            yield tx
    finally:
        _IN_TRANSACTION.active = was_active


# ---- Strict id validation ------------------------------------------------

_ID_PATTERNS = {
    "run": re.compile(r"^run_[0-9a-f]{12}$"),
    "task": re.compile(r"^task_[0-9a-f]{12}$"),
    "feedback": re.compile(r"^fb_[0-9a-f]{12}$"),
    "prompt": re.compile(r"^prompt_v\d{1,6}$"),
    "case": re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_-]{0,99}$"),
}


def valid_id(kind: str, value: str) -> bool:
    """True when value matches the anchored id pattern for kind."""
    pattern = _ID_PATTERNS.get(kind)
    if pattern is None:
        raise ValueError(f"Unknown id kind: {kind!r}")
    return bool(value) and bool(pattern.fullmatch(value))


def require_id(kind: str, value: str) -> str:
    """Return value if valid for kind, else raise ValueError."""
    if not valid_id(kind, value):
        raise ValueError(f"Invalid {kind} id: {value!r}")
    return value
