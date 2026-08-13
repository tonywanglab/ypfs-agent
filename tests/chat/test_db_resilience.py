"""Recovery from a dropped database connection.

A hosted Postgres closes idle connections. Before these fixes, the first request
afterwards raised psycopg.OperationalError straight out of a Flask view — the
operator got a 500 on the page they were looking at, from a context processor
that runs on every render.
"""

from __future__ import annotations

import psycopg
import pytest

from harness import dbio, web


def test_query_retries_once_on_a_dropped_connection(pg, monkeypatch):
    calls = {"n": 0}
    real_conn = dbio._conn()

    def flaky_conn():
        calls["n"] += 1
        if calls["n"] == 1:
            raise psycopg.OperationalError(
                "consuming input failed: server closed the connection unexpectedly")
        return real_conn

    monkeypatch.setattr(dbio, "_conn", flaky_conn)
    monkeypatch.setattr(dbio, "reset_conn", lambda: None)

    assert dbio.q1("SELECT 1 AS ok")["ok"] == 1
    assert calls["n"] == 2, "should have retried exactly once on a fresh connection"


def test_a_dropped_connection_is_discarded_before_the_retry(pg, monkeypatch):
    """Retrying on the same dead handle is what spun forever in production."""
    resets = []
    calls = {"n": 0}
    real_conn = dbio._conn()

    def flaky_conn():
        calls["n"] += 1
        if calls["n"] == 1:
            raise psycopg.OperationalError("server closed the connection unexpectedly")
        return real_conn

    monkeypatch.setattr(dbio, "_conn", flaky_conn)
    monkeypatch.setattr(dbio, "reset_conn", lambda: resets.append(True))

    dbio.q1("SELECT 1 AS ok")
    assert resets == [True]


def test_a_real_query_error_is_not_retried(pg):
    """A bad query must surface, not get silently run twice."""
    with pytest.raises(psycopg.errors.UndefinedTable):
        dbio.q("SELECT * FROM a_table_that_does_not_exist")


def test_retry_does_not_happen_inside_a_transaction(pg, monkeypatch):
    """Re-running one statement of a multi-statement transaction on a new
    connection would silently drop the statements before it."""
    calls = {"n": 0}
    real_conn = dbio._conn()

    def flaky_conn():
        calls["n"] += 1
        if calls["n"] > 1:
            raise psycopg.OperationalError("server closed the connection unexpectedly")
        return real_conn

    with pytest.raises(psycopg.OperationalError):
        with dbio.transaction():
            monkeypatch.setattr(dbio, "_conn", flaky_conn)
            calls["n"] = 1  # next _conn() call raises
            dbio.execute("SELECT 1")


def test_transaction_flag_is_cleared_after_the_block(pg):
    assert not getattr(dbio._IN_TRANSACTION, "active", False)
    with dbio.transaction():
        assert dbio._IN_TRANSACTION.active is True
    assert dbio._IN_TRANSACTION.active is False

    # And after a failure inside the block.
    with pytest.raises(RuntimeError):
        with dbio.transaction():
            raise RuntimeError("boom")
    assert dbio._IN_TRANSACTION.active is False


def test_transaction_still_commits_and_rolls_back(pg):
    """The contextmanager wrapper must not change transaction semantics."""
    from harness import seed
    from harness.models import Case

    with dbio.transaction():
        seed.insert_case(Case(case_id="committed_case", prompt="q"))
    assert dbio.q1("SELECT 1 FROM cases WHERE case_id = 'committed_case'") is not None

    with pytest.raises(RuntimeError):
        with dbio.transaction():
            seed.insert_case(Case(case_id="rolled_back_case", prompt="q"))
            raise RuntimeError("abort")
    assert dbio.q1("SELECT 1 FROM cases WHERE case_id = 'rolled_back_case'") is None


def test_login_page_survives_a_database_outage(seeded, monkeypatch):
    """The exact 500 seen in the dev-server log: a context processor that runs
    on every render hit a dead connection and took /login down with it."""
    monkeypatch.setenv("HARNESS_ADMIN_PASSWORD", "pw")
    client = web.create_app().test_client()

    from harness import versions

    def database_is_gone():
        raise psycopg.OperationalError("server closed the connection unexpectedly")

    monkeypatch.setattr(versions, "latest_prompt_id", database_is_gone)

    response = client.get("/login")
    assert response.status_code == 200
    assert "Admin sign-in" in response.get_data(as_text=True)
