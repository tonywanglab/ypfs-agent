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


def q(sql: str, params: tuple | dict = ()) -> list[dict]:
    """Run a SELECT and return all rows as dicts."""
    from psycopg.rows import dict_row
    with _conn().cursor(row_factory=dict_row) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def q1(sql: str, params: tuple | dict = ()) -> dict | None:
    """Run a SELECT (or RETURNING statement) and return the first row or None."""
    rows = q(sql, params)
    return rows[0] if rows else None


def execute(sql: str, params: tuple | dict = ()) -> int:
    """Run a statement; returns the affected row count."""
    with _conn().cursor() as cur:
        cur.execute(sql, params)
        return cur.rowcount


def transaction():
    """Explicit transaction block for multi-statement writes.

    Usage: `with dbio.transaction():` — psycopg issues BEGIN/COMMIT around the
    block even on an autocommit connection.
    """
    return _conn().transaction()


# ---- Strict id validation ------------------------------------------------

_ID_PATTERNS = {
    "run": re.compile(r"^run_[0-9a-f]{12}$"),
    "task": re.compile(r"^task_[0-9a-f]{12}$"),
    "review": re.compile(r"^rev_[0-9a-f]{12}$"),
    "prompt": re.compile(r"^prompt_v\d{1,6}$"),
    "rubric": re.compile(r"^rubric_v\d{1,6}$"),
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
