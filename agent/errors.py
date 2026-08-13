"""
Persist agent/tool runtime errors to Postgres for observability.

`log_error` writes one row to the `agent_errors` table (see schema.sql). It is
deliberately fail-safe: anything that goes wrong while logging — no DATABASE_URL,
DB unreachable, missing table — is swallowed (with a one-line stderr warning) so
error logging can never take down the agent loop it is observing.

With no DATABASE_URL set it is a silent no-op, so `run()` stays usable in tests
and evals without a Postgres dependency.
"""

import json
import os
import sys
from pathlib import Path

# db.py lives at the repo root, one level up from this package.
sys.path.insert(0, str(Path(__file__).parent.parent))

_INSERT = (
    "INSERT INTO agent_errors (run_id, error_type, tool_name, message, context) "
    "VALUES (%s, %s, %s, %s, %s)"
)


def log_error(run_id: str, error_type: str, message: str,
              tool_name: str | None = None, context: dict | None = None) -> None:
    """Write one agent_errors row. Never raises.

    error_type is one of 'tool_error' | 'api_error' | 'max_steps'. context is a
    small dict (args, model, step, status code, …) stored as jsonb.
    """
    if not os.getenv("DATABASE_URL"):
        return  # no store configured -> no-op
    try:
        import db
        from psycopg.types.json import Jsonb

        conn = db.get_conn()
        payload = Jsonb(context) if context is not None else None
        with conn.cursor() as cur:
            cur.execute(_INSERT, (run_id, error_type, tool_name, message[:8000], payload))
    except Exception as e:  # logging must never break the loop
        print(f"[errors] failed to log {error_type}: {type(e).__name__}: {e}",
              file=sys.stderr)
