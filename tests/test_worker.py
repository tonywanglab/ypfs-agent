from __future__ import annotations

import threading
import time

import requests

from harness import llm, seed, tasks, versions, worker
from harness import runner as runner_module
from harness.models import Case


def _patch_agent_pipeline(monkeypatch, answer="answer"):
    calls = {"n": 0}

    def fake_agent_run(user_msg, history, model, system_prompt, context=None):
        calls["n"] += 1
        return answer, []

    monkeypatch.setattr(runner_module, "agent_run", fake_agent_run)
    return calls


def test_progress_message_single_sample_by_phase():
    assert worker._progress_message("prepare", current_sample=0, completed_samples=0, samples=1) \
        == "Preparing run…"
    assert worker._progress_message("agent", current_sample=1, completed_samples=0, samples=1) \
        == "Running agent…"
    assert worker._progress_message("sample_done", current_sample=1, completed_samples=1, samples=1) \
        == "Sample complete."


def test_progress_message_multi_sample():
    assert worker._progress_message(
        "agent", current_sample=2, completed_samples=1, samples=5,
    ) == "Sample 2 of 5 — Running agent…"
    assert worker._progress_message(
        "prepare", current_sample=0, completed_samples=0, samples=5,
    ) == "Preparing 5 samples…"
    assert worker._progress_message(
        "sample_done", current_sample=3, completed_samples=3, samples=5,
    ) == "Sample 3 of 5 complete."
    assert worker._progress_message(
        "sample_done", current_sample=5, completed_samples=5, samples=5,
    ) == "All 5 samples complete — saving run…"


def test_error_message_for_missing_openrouter_key():
    exc = KeyError("OPENROUTER_API_KEY")
    assert "OPENROUTER_API_KEY is not set" in worker._error_message(exc)


def test_error_message_for_http_error():
    response = requests.Response()
    response.status_code = 429
    response._content = b"rate limited"
    exc = requests.HTTPError(response=response)
    message = worker._error_message(exc)
    assert "429" in message
    assert "rate limited" in message


def test_error_message_fallback():
    assert worker._error_message(RuntimeError("boom")) == "Task failed: boom"


def test_execute_task_runs_experiment_and_finishes_with_run_id(pg, monkeypatch):
    seed.seed_prompt_v1()
    _patch_agent_pipeline(monkeypatch)

    case = Case("case_1", "question")
    payload = {
        "case": case.to_dict(),
        "prompt_id": "prompt_v1",
        "samples": 1,
    }
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, payload)
    claimed = tasks.claim("worker-1")

    worker.execute_task(claimed)

    loaded = tasks.load(enqueued["task_id"])
    assert loaded["status"] == "finished"
    assert loaded["run_id"]
    assert loaded["result"] == {"run_id": loaded["run_id"]}
    assert loaded["progress"]["phase"] == "sample_done"
    assert loaded["error"] is None


def test_execute_task_reports_progress_as_it_goes(pg, monkeypatch):
    seed.seed_prompt_v1()
    _patch_agent_pipeline(monkeypatch)

    case = Case("case_1", "question")
    payload = {
        "case": case.to_dict(),
        "prompt_id": "prompt_v1",
        "samples": 2,
    }
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, payload)
    claimed = tasks.claim("worker-1")

    seen_phases = []
    orig_set_progress = tasks.set_progress

    def spy_set_progress(task_id, **fields):
        seen_phases.append(fields.get("phase"))
        orig_set_progress(task_id, **fields)

    monkeypatch.setattr(tasks, "set_progress", spy_set_progress)
    worker.execute_task(claimed)

    assert seen_phases[0] == "prepare"
    assert seen_phases[-1] == "sample_done"
    assert "agent" in seen_phases
    loaded = tasks.load(enqueued["task_id"])
    assert loaded["status"] == "finished"


def test_execute_task_prompt_draft_finishes_with_draft_result(pg, monkeypatch):
    seed.seed_prompt_v1()
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "drafted prompt",
        "rationale": "fix it",
    })
    monkeypatch.setattr(versions, "_feedback_context", lambda feedback_ids: [{"stub": True}])

    enqueued = tasks.enqueue(tasks.KIND_PROMPT_DRAFT, {"base_id": "prompt_v1", "feedback_ids": ["fb_stub"]})
    claimed = tasks.claim("worker-1")

    worker.execute_task(claimed)

    loaded = tasks.load(enqueued["task_id"])
    assert loaded["status"] == "finished"
    assert loaded["result"]["prompt_text"] == "drafted prompt"
    assert loaded["result"]["base_id"] == "prompt_v1"


def test_execute_task_expected_error_fails_task_with_readable_message(pg, monkeypatch):
    seed.seed_prompt_v1()

    def raise_value_error(*args, **kwargs):
        raise ValueError("bad case payload")

    monkeypatch.setattr(runner_module, "agent_run", raise_value_error)

    case = Case("case_1", "question")
    payload = {
        "case": case.to_dict(),
        "prompt_id": "prompt_v1",
        "samples": 1,
    }
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, payload)
    claimed = tasks.claim("worker-1")

    worker.execute_task(claimed)  # must not raise

    loaded = tasks.load(enqueued["task_id"])
    assert loaded["status"] == "failed"
    assert "bad case payload" in loaded["error"]


def test_execute_task_unexpected_error_fails_task_and_does_not_raise(pg, monkeypatch):
    seed.seed_prompt_v1()

    def raise_type_error(*args, **kwargs):
        raise TypeError("totally unexpected")

    monkeypatch.setattr(runner_module, "agent_run", raise_type_error)

    case = Case("case_1", "question")
    payload = {
        "case": case.to_dict(),
        "prompt_id": "prompt_v1",
        "samples": 1,
    }
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, payload)
    claimed = tasks.claim("worker-1")

    worker.execute_task(claimed)  # must not raise, even for an unexpected error type

    loaded = tasks.load(enqueued["task_id"])
    assert loaded["status"] == "failed"
    assert "internal error" in loaded["error"]
    assert "TypeError" in loaded["error"]


def test_execute_task_unknown_kind_fails_immediately(pg):
    row = tasks.enqueue(tasks.KIND_EXPERIMENT, {"query": "q"})
    claimed = tasks.claim("worker-1")
    claimed["kind"] = "not_a_real_kind"

    worker.execute_task(claimed)

    loaded = tasks.load(row["task_id"])
    assert loaded["status"] == "failed"
    assert "Unknown task kind" in loaded["error"]


def test_worker_loop_claims_executes_and_stops(pg, monkeypatch):
    seed.seed_prompt_v1()
    _patch_agent_pipeline(monkeypatch)

    case = Case("case_1", "question")
    payload = {
        "case": case.to_dict(),
        "prompt_id": "prompt_v1",
        "samples": 1,
    }
    enqueued = tasks.enqueue(tasks.KIND_EXPERIMENT, payload)

    stop_event = threading.Event()
    thread = threading.Thread(target=worker.worker_loop, args=("test-worker", stop_event))
    thread.start()
    try:
        for _ in range(50):
            loaded = tasks.load(enqueued["task_id"])
            if loaded["status"] in ("finished", "failed"):
                break
            time.sleep(0.1)
        else:
            raise AssertionError("worker_loop did not finish the task in time")
    finally:
        stop_event.set()
        thread.join(timeout=5.0)

    loaded = tasks.load(enqueued["task_id"])
    assert loaded["status"] == "finished"
