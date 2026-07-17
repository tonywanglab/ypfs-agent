"""Shared pytest fixtures for the harness test suite.

Every test that touches harness storage gets an isolated Postgres schema:
a throwaway schema is created, schema.sql is applied inside it, and
db.get_thread_conn is monkeypatched so every harness.dbio call lands there
instead of the real database. Dropped on teardown.
"""

from __future__ import annotations

import os
import secrets
import threading

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture()
def pg(monkeypatch):
    """Isolated Postgres schema per test. Skips when no DB URL is configured."""
    url = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL/DATABASE_URL not set")

    import psycopg
    from pgvector.psycopg import register_vector

    import db as db_module

    schema = f"test_{secrets.token_hex(6)}"
    admin_conn = psycopg.connect(url, autocommit=True, prepare_threshold=None)
    admin_conn.execute(f'CREATE SCHEMA "{schema}"')

    ddl = db_module.SCHEMA_PATH.read_text().replace("{{DIM}}", "1536")
    local = threading.local()

    def get_test_conn():
        # Mirrors db.get_thread_conn(): one real connection per thread, so
        # concurrent-claim tests (separate threads) never share a psycopg
        # connection, which isn't safe for concurrent use.
        conn = getattr(local, "conn", None)
        if conn is not None and not conn.closed:
            return conn
        conn = psycopg.connect(
            url,
            autocommit=True,
            prepare_threshold=None,
            options=f'-c search_path="{schema}",public',
        )
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            if cur.fetchone() is None:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)
        local.conn = conn
        return conn

    setup_conn = get_test_conn()
    setup_conn.execute(ddl)

    monkeypatch.setattr(db_module, "get_thread_conn", get_test_conn)

    try:
        yield schema
    finally:
        admin_conn.execute(f'DROP SCHEMA "{schema}" CASCADE')
        admin_conn.close()


@pytest.fixture()
def make_run(pg):
    """Factory: make_run(run_id, prompt_id, rubric_id) inserts a minimal
    case+run row (bypassing the agent pipeline), for tests that only need a
    real run to satisfy reviews.run_id's foreign key. Ensures the default
    prompt_v1/rubric_v1 baseline exists; pass a different id only if the
    test already created that version itself."""
    from harness.models import Case, RunManifest
    from harness.runner import save_manifest
    from harness.seed import insert_case, seed_prompt_v1, seed_rubric_v1

    def _make(run_id="run_1", prompt_id="prompt_v1", rubric_id="rubric_v1", case_id=None):
        if prompt_id == "prompt_v1":
            seed_prompt_v1()
        if rubric_id == "rubric_v1":
            seed_rubric_v1()
        case_id = case_id or f"case_for_{run_id}"
        insert_case(Case(case_id=case_id, prompt="test question"))
        manifest = RunManifest(
            run_id=run_id,
            case_id=case_id,
            agent_model="test-agent",
            judge_model="test-judge",
            prompt_id=prompt_id,
            rubric_id=rubric_id,
            created_at="2024-01-01T00:00:00Z",
            status="pending",
            sample_count=1,
        )
        save_manifest(
            manifest,
            case_snapshot={"case_id": case_id, "prompt": "test question", "tags": [], "notes": ""},
        )
        return run_id

    return _make
