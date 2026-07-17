"""Queue worker: claims tasks from Postgres and executes them.

Run as `python -m harness worker --concurrency 3` (its own process, the shape
that also works under gunicorn deployments), or in-process for one-command dev
via `python -m harness web --with-worker`.

Each worker thread loops: requeue stale claims -> claim one task -> execute it
under a heartbeat -> mark finished/failed. Expected failures (bad input,
OpenRouter errors) fail the task with a readable message; unexpected ones fail
the task and keep the worker alive.
"""

from __future__ import annotations

import random
import threading

import requests

from agent.context import RunContext

from . import tasks, versions
from .models import Case
from .runner import run_case_samples

CLAIM_POLL_INTERVAL_S = 1.0
HEARTBEAT_INTERVAL_S = 15.0

EXPECTED_ERRORS = (KeyError, requests.RequestException, RuntimeError, ValueError,
                   FileNotFoundError)


def _error_message(exc: BaseException) -> str:
    if isinstance(exc, KeyError) and exc.args and exc.args[0] == "OPENROUTER_API_KEY":
        return "OPENROUTER_API_KEY is not set. Add it to .env and restart the worker."
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return f"OpenRouter request failed ({exc.response.status_code}): {exc.response.text[:200]}"
    return f"Task failed: {exc}"


def _progress_message(phase: str, *, current_sample: int, completed_samples: int,
                      samples: int) -> str:
    phase_labels = {
        "prepare": "Preparing run…",
        "agent": "Running agent…",
        "checks": "Running deterministic checks…",
        "judge": "Judging answer…",
        "sample_done": "Sample complete.",
    }
    label = phase_labels.get(phase, "Working…")
    if samples <= 1:
        return label
    if phase == "prepare":
        return f"Preparing {samples} samples…"
    if phase == "sample_done":
        if completed_samples >= samples:
            return f"All {samples} samples complete — saving run…"
        return f"Sample {completed_samples} of {samples} complete."
    return f"Sample {current_sample} of {samples} — {label}"


def _execute_experiment(task: dict) -> None:
    payload = task["payload"]
    case = Case.from_dict(payload["case"])
    prompt = versions.load_prompt(payload["prompt_id"])
    rubric = versions.load_rubric(payload["rubric_id"])
    samples = int(payload.get("samples", 1))

    def on_progress(phase, sample_index, sample_total, run_id):
        completed = sample_index if phase == "sample_done" else max(0, sample_index - 1)
        current = sample_index if phase != "prepare" else 0
        if run_id:
            tasks.set_run(task["task_id"], run_id)
        tasks.set_progress(
            task["task_id"],
            phase=phase,
            current_sample=current,
            completed_samples=completed,
            message=_progress_message(
                phase,
                current_sample=current,
                completed_samples=completed,
                samples=samples,
            ),
        )

    manifest = run_case_samples(
        case,
        prompt.text,
        prompt.prompt_id,
        rubric,
        samples=samples,
        on_progress=on_progress,
        context=RunContext(),
    )
    tasks.set_run(task["task_id"], manifest.run_id)
    tasks.finish(task["task_id"], result={"run_id": manifest.run_id})


def _execute_prompt_draft(task: dict) -> None:
    payload = task["payload"]
    draft = versions.draft_prompt(payload["base_id"], payload.get("review_ids", []))
    tasks.finish(task["task_id"], result=draft)


def _execute_rubric_draft(task: dict) -> None:
    payload = task["payload"]
    draft = versions.draft_rubric(payload["base_id"], payload.get("review_ids", []))
    tasks.finish(task["task_id"], result=draft)


EXECUTORS = {
    tasks.KIND_EXPERIMENT: _execute_experiment,
    tasks.KIND_PROMPT_DRAFT: _execute_prompt_draft,
    tasks.KIND_RUBRIC_DRAFT: _execute_rubric_draft,
}


def _start_heartbeat(task_id: str, stop: threading.Event) -> threading.Thread:
    def beat():
        while not stop.wait(HEARTBEAT_INTERVAL_S):
            tasks.heartbeat(task_id)

    thread = threading.Thread(target=beat, name=f"heartbeat-{task_id}", daemon=True)
    thread.start()
    return thread


def execute_task(task: dict) -> None:
    """Run one claimed task to completion (finished or failed). Exposed for
    tests and for driving the queue synchronously."""
    executor = EXECUTORS.get(task["kind"])
    if executor is None:
        tasks.fail(task["task_id"], f"Unknown task kind: {task['kind']!r}")
        return
    hb_stop = threading.Event()
    hb_thread = _start_heartbeat(task["task_id"], hb_stop)
    try:
        executor(task)
    except EXPECTED_ERRORS as exc:
        tasks.fail(task["task_id"], _error_message(exc))
    except Exception as exc:  # unexpected: fail the task, keep the worker alive
        tasks.fail(task["task_id"], f"internal error: {type(exc).__name__}: {exc}")
    finally:
        hb_stop.set()
        hb_thread.join(timeout=1.0)


def worker_loop(name: str, stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        try:
            tasks.requeue_stale()
            task = tasks.claim(name)
        except Exception as exc:  # DB hiccup: back off and retry
            print(f"[{name}] queue error: {exc}")
            stop_event.wait(5.0)
            continue
        if task is None:
            stop_event.wait(CLAIM_POLL_INTERVAL_S + random.random())
            continue
        print(f"[{name}] claimed {task['task_id']} ({task['kind']})")
        execute_task(task)
        print(f"[{name}] done {task['task_id']}")


def start_workers(concurrency: int, stop_event: threading.Event,
                  daemon: bool = False) -> list[threading.Thread]:
    threads = []
    for i in range(concurrency):
        thread = threading.Thread(
            target=worker_loop,
            args=(f"worker-{i + 1}", stop_event),
            name=f"worker-{i + 1}",
            daemon=daemon,
        )
        thread.start()
        threads.append(thread)
    return threads


def main(concurrency: int = 3) -> None:
    import signal

    stop_event = threading.Event()

    def handle_signal(signum, frame):
        print("\nStopping after in-flight tasks…")
        stop_event.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print(f"Worker pool: {concurrency} thread(s), polling for tasks. Ctrl-C to stop.")
    threads = start_workers(concurrency, stop_event)
    for thread in threads:
        thread.join()
