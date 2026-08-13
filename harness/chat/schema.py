"""Apply the chat feature's DDL.

Deliberately separate from db.init_schema()/schema.sql: the chat tables are an
opt-in addition, so installing them is its own command (`python -m harness
chat-init`) and the eval harness's schema path is untouched. The DDL is
additive-only (CREATE ... IF NOT EXISTS), which is what makes both this and
its rollback safe to run against a live database.
"""

from __future__ import annotations

from pathlib import Path

from .. import dbio
from ..storage import REPO_ROOT

MIGRATIONS_DIR = REPO_ROOT / "migrations" / "chat"
SCHEMA_PATH = MIGRATIONS_DIR / "001_chat_schema.sql"
ROLLBACK_PATH = MIGRATIONS_DIR / "999_rollback.sql"

# The tables 001 creates, in dependency order — used to report what exists.
CHAT_TABLES = (
    "chat_conversations",
    "chat_turns",
    "chat_run_links",
    "chat_prompt_revisions",
    "chat_golden_pairs",
)


def _run_sql_file(path: Path) -> None:
    """Execute a whole .sql file in one call.

    psycopg falls back to the simple query protocol when execute() gets no
    parameters, which is what allows a multi-statement script here. Same
    mechanism db.init_schema() relies on for schema.sql.
    """
    dbio.execute(path.read_text())


def init_chat_schema() -> None:
    """Create the chat tables if they don't exist. Idempotent."""
    _run_sql_file(SCHEMA_PATH)


def drop_chat_schema() -> None:
    """Drop every chat table. Destructive; exposed for tests and teardown."""
    _run_sql_file(ROLLBACK_PATH)


def installed_tables() -> list[str]:
    """Which chat tables currently exist in the search_path."""
    rows = dbio.q(
        """
        SELECT table_name FROM information_schema.tables
         WHERE table_name = ANY(%s)
           AND table_schema = ANY(current_schemas(false))
        """,
        (list(CHAT_TABLES),),
    )
    found = {row["table_name"] for row in rows}
    return [name for name in CHAT_TABLES if name in found]


def is_installed() -> bool:
    """True once every chat table exists.

    The blueprint uses this to fail with a readable "run chat-init" message
    instead of a raw UndefinedTable error.
    """
    return len(installed_tables()) == len(CHAT_TABLES)
