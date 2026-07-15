from __future__ import annotations

import threading

import pytest

from harness import registry


def test_load_creates_default(evals_dir):
    data = registry.load()
    assert data["active_rubric_id"] == "rubric_v1"
    assert data["active_prompt_id"] == "prompt_v1"
    assert data["cycle"]["locked_branch"] is None
    assert registry.REGISTRY_PATH.exists()


def test_lock_cycle_then_conflicting_branch_raises(evals_dir):
    registry.lock_cycle("rubric")
    assert registry.locked_branch() == "rubric"
    with pytest.raises(registry.CycleLockedError):
        registry.lock_cycle("prompt")


def test_lock_cycle_same_branch_is_idempotent(evals_dir):
    registry.lock_cycle("rubric")
    registry.lock_cycle("rubric")  # should not raise
    assert registry.locked_branch() == "rubric"


def test_enqueue_and_dequeue(evals_dir):
    registry.enqueue("prompt", "review_rev1")
    assert registry.pending_queue()["prompt"] == ["review_rev1"]
    registry.enqueue("prompt", "review_rev1")  # no duplicate
    assert registry.pending_queue()["prompt"] == ["review_rev1"]
    registry.dequeue("prompt", "review_rev1")
    assert registry.pending_queue()["prompt"] == []


def test_close_cycle_unlocks_and_archives_history(evals_dir):
    registry.lock_cycle("rubric", opened_by="supervisor")
    registry.close_cycle(decision="approved")
    data = registry.load()
    assert data["cycle"]["locked_branch"] is None
    assert len(data["history"]) == 1
    assert data["history"][0]["locked_branch"] == "rubric"
    assert data["history"][0]["decision"] == "approved"

    # Now the other branch can proceed.
    registry.lock_cycle("prompt")
    assert registry.locked_branch() == "prompt"


def test_set_active_rubric_and_prompt(evals_dir):
    registry.set_active_rubric("rubric_v2")
    registry.set_active_prompt("prompt_v3")
    data = registry.load()
    assert data["active_rubric_id"] == "rubric_v2"
    assert data["active_prompt_id"] == "prompt_v3"


def test_concurrent_registry_updates_do_not_lose_changes(evals_dir, monkeypatch):
    registry.load()
    original_load = registry.load
    reads_complete = threading.Barrier(2)

    def synchronized_load():
        data = original_load()
        reads_complete.wait(timeout=2)
        return data

    monkeypatch.setattr(registry, "load", synchronized_load)
    rubric_thread = threading.Thread(
        target=registry.set_active_rubric,
        args=("rubric_v2",),
    )
    prompt_thread = threading.Thread(
        target=registry.set_active_prompt,
        args=("prompt_v3",),
    )
    rubric_thread.start()
    prompt_thread.start()
    rubric_thread.join(timeout=3)
    prompt_thread.join(timeout=3)

    assert not rubric_thread.is_alive()
    assert not prompt_thread.is_alive()
    data = original_load()
    assert data["active_rubric_id"] == "rubric_v2"
    assert data["active_prompt_id"] == "prompt_v3"
