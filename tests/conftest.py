"""Shared pytest fixtures for the harness test suite.

Every test that touches harness storage gets an isolated Postgres schema,
but the physical connection is shared across the whole test session and
reused (via db.get_thread_conn monkeypatched to hand back that connection)
rather than opened fresh per test. Rapidly opening/closing many physical
connections in one process has been observed to segfault psycopg_binary on
this environment (Python 3.14 + psycopg-binary 3.3.4) — see the long-running
`harness web`/`worker` processes, which never crash, for contrast. Threads a
test spawns itself still get their own real connection, since psycopg
connections aren't safe for concurrent use across threads.
"""

from __future__ import annotations

import os
import secrets
import threading

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def _pg_url():
    url = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL/DATABASE_URL not set")
    return url


@pytest.fixture(scope="session")
def _shared_conn(_pg_url):
    import psycopg

    conn = psycopg.connect(_pg_url, autocommit=True, prepare_threshold=None)
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        if cur.fetchone() is None:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # No register_vector(): none of the harness DB tests touch the
    # `chunks.embedding` vector column.
    yield conn
    conn.close()


@pytest.fixture()
def pg(_pg_url, _shared_conn, monkeypatch):
    """Isolated Postgres schema per test on the shared session connection."""
    import db as db_module

    schema = f"test_{secrets.token_hex(6)}"
    _shared_conn.execute(f'CREATE SCHEMA "{schema}"')
    _shared_conn.execute(f'SET search_path TO "{schema}", public')

    ddl = db_module.SCHEMA_PATH.read_text().replace("{{DIM}}", "1536")
    _shared_conn.execute(ddl)

    main_thread_id = threading.get_ident()
    local = threading.local()

    def get_test_conn():
        if threading.get_ident() == main_thread_id:
            return _shared_conn
        # A thread the test spawned itself: give it its own real connection
        # scoped to the same schema, cached for the life of that thread.
        conn = getattr(local, "conn", None)
        if conn is not None and not conn.closed:
            return conn
        import psycopg

        conn = psycopg.connect(
            _pg_url,
            autocommit=True,
            prepare_threshold=None,
            options=f'-c search_path="{schema}",public',
        )
        local.conn = conn
        return conn

    monkeypatch.setattr(db_module, "get_thread_conn", get_test_conn)

    try:
        yield schema
    finally:
        _shared_conn.execute(f'DROP SCHEMA "{schema}" CASCADE')


@pytest.fixture()
def make_run(pg):
    """Factory: make_run(run_id, prompt_id) inserts a minimal case+run+sample
    row (bypassing the agent pipeline), for tests that only need a real run
    to satisfy feedback.run_id's foreign key or exercise run_detail/feedback
    routes. Ensures the default prompt_v1 baseline exists; pass a different
    id only if the test already created that version itself."""
    from harness import dbio
    from harness.models import Case, RunManifest
    from harness.runner import save_manifest
    from harness.seed import insert_case, seed_prompt_v1

    def _make(run_id="run_1", prompt_id="prompt_v1", case_id=None, answer="test answer"):
        if prompt_id == "prompt_v1":
            seed_prompt_v1()
        case_id = case_id or f"case_for_{run_id}"
        insert_case(Case(case_id=case_id, prompt="test question"))
        manifest = RunManifest(
            run_id=run_id,
            case_id=case_id,
            agent_model="test-agent",
            prompt_id=prompt_id,
            created_at="2024-01-01T00:00:00Z",
            status="complete",
            sample_count=1,
        )
        save_manifest(
            manifest,
            case_snapshot={"case_id": case_id, "prompt": "test question", "tags": [], "notes": ""},
        )
        dbio.execute(
            "INSERT INTO run_samples (run_id, sample_index, answer, trace) VALUES (%s, %s, %s, %s)",
            (run_id, 1, answer, dbio.jsonb({"tool_calls": []})),
        )
        return run_id

    return _make
