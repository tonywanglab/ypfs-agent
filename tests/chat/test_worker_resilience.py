"""Regression tests for the failure modes a live dev-server session exposed.

Two things went wrong in real use and both are covered here:

1. A worker running older code claimed a chat task, didn't recognize the kind,
   and failed it with "Unknown task kind". The executor registration in
   harness/worker.py is what must not silently go missing.
2. When the database connection dropped, the claim loop retried forever on the
   same poisoned connection at a flat interval, exhausting local ephemeral ports
   and taking the process down.
"""

from __future__ import annotations

import threading

from harness import dbio, tasks, worker


def test_chat_kinds_have_executors_registered():
    """If this registration is ever skipped, chat tasks get claimed and failed
    with "Unknown task kind" — which reads like a queue bug, not an import bug."""
    assert tasks.KIND_CHAT_TURN in worker.EXECUTORS
    assert tasks.KIND_CHAT_REGENERATE in worker.EXECUTORS
    assert worker.EXECUTORS[tasks.KIND_CHAT_TURN] is not None


def test_every_declared_kind_is_executable():
    """tasks.KINDS and worker.EXECUTORS must agree. A kind that can be enqueued
    but not executed is a task that always fails."""
    assert set(tasks.KINDS) == set(worker.EXECUTORS)


def test_unknown_kind_still_fails_the_task_rather_than_the_worker(pg):
    """The behavior a stale worker hit. It should fail that task and stay alive."""
    row = dbio.q1(
        "INSERT INTO tasks (task_id, kind, status, payload) "
        "VALUES (%s, 'from_the_future', 'running', '{}') RETURNING *",
        (tasks.new_task_id(),),
    )
    worker.execute_task(tasks.task_payload(row))
    reloaded = tasks.load(row["task_id"])
    assert reloaded["status"] == "failed"
    assert "Unknown task kind" in reloaded["error"]


def test_reset_conn_is_safe_with_no_connection(pg):
    dbio.reset_conn()
    dbio.reset_conn()
    # The next query still works: reset only discards the cached handle.
    assert dbio.q1("SELECT 1 AS ok")["ok"] == 1


def test_queue_errors_discard_the_connection_and_back_off(pg, monkeypatch):
    """A database error must throw the connection away and widen the wait.

    Retrying on the same handle was the actual bug: a connection left holding an
    unconsumed result fails identically forever, and a flat retry against an
    unreachable server burns ephemeral ports until the host runs out.
    """
    resets = []
    waits = []
    monkeypatch.setattr(dbio, "reset_conn", lambda: resets.append(True))

    def always_fails():
        raise RuntimeError("could not receive data from server")

    monkeypatch.setattr(worker.tasks, "requeue_stale", always_fails)

    stop = threading.Event()

    class FakeStop:
        def is_set(self):
            return len(waits) >= 4

        def wait(self, timeout):
            waits.append(timeout)
            return False

    worker.worker_loop("test-worker", FakeStop())

    assert len(resets) == 4, "each failure must discard the connection"
    # Doubling, capped.
    assert waits[0] == worker.QUEUE_ERROR_BACKOFF_S
    assert waits[1] == worker.QUEUE_ERROR_BACKOFF_S * 2
    assert waits[2] == worker.QUEUE_ERROR_BACKOFF_S * 4
    assert all(w <= worker.QUEUE_ERROR_BACKOFF_MAX_S for w in waits)
    assert waits == sorted(waits), "backoff must not shrink while failing"
    stop.set()


def test_backoff_resets_after_a_successful_claim(pg, monkeypatch):
    """One transient blip must not leave the worker slow forever."""
    waits = []
    calls = {"n": 0}
    monkeypatch.setattr(dbio, "reset_conn", lambda: None)

    def flaky():
        calls["n"] += 1
        if calls["n"] in (1, 2):
            raise RuntimeError("transient")

    monkeypatch.setattr(worker.tasks, "requeue_stale", flaky)
    monkeypatch.setattr(worker.tasks, "claim", lambda name: None)

    class FakeStop:
        def is_set(self):
            return len(waits) >= 5

        def wait(self, timeout):
            waits.append(timeout)
            return False

    worker.worker_loop("test-worker", FakeStop())

    # Two failures double the backoff, then success drops back to the short
    # idle poll interval.
    assert waits[0] == worker.QUEUE_ERROR_BACKOFF_S
    assert waits[1] == worker.QUEUE_ERROR_BACKOFF_S * 2
    assert waits[2] < worker.QUEUE_ERROR_BACKOFF_S
