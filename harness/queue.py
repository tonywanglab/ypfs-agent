"""Evaluation job queue: enqueue query-answer work and process concurrently.

All durable job state lives under evals/jobs/. The web layer reads a trimmed
public status view via jobs.public_status_payload() and never owns pipeline
state separately (no evals/experiments/ mirror).
"""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

import requests

from . import config, jobs, versions
from .models import Case
from .runner import RunPhase, run_case_samples
from .storage import new_id, now_iso

KIND_EXPERIMENT = jobs.KIND_EXPERIMENT
KIND_PROMPT_DRAFT = jobs.KIND_PROMPT_DRAFT
KIND_RUBRIC_DRAFT = jobs.KIND_RUBRIC_DRAFT

DEFAULT_MAX_WORKERS = max(1, int(os.environ.get("HARNESS_QUEUE_WORKERS", "3")))

_executor: ThreadPoolExecutor | None = None
_executor_lock = threading.Lock()


def _progress_message(
    phase: str,
    *,
    current_sample: int,
    completed_samples: int,
    samples: int,
) -> str:
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


def _run_error_message(exc: BaseException) -> str:
    if isinstance(exc, KeyError) and exc.args and exc.args[0] == "OPENROUTER_API_KEY":
        return "OPENROUTER_API_KEY is not set. Add it to .env and restart the server."
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return (
            f"OpenRouter request failed ({exc.response.status_code}): "
            f"{exc.response.text[:200]}"
        )
    return f"Run failed: {exc}"


def _update_progress(
    job_id: str,
    *,
    phase: str,
    current_sample: int,
    completed_samples: int,
    run_id: str | None = None,
) -> None:
    job = jobs.load_job(job_id)
    samples = int(job.get("samples", 1))
    fields: dict[str, Any] = {
        "phase": phase,
        "current_sample": current_sample,
        "completed_samples": completed_samples,
        "message": _progress_message(
            phase,
            current_sample=current_sample,
            completed_samples=completed_samples,
            samples=samples,
        ),
    }
    if run_id:
        fields["run_id"] = run_id
    jobs.update_job(job_id, **fields)


def _process_experiment(job_id: str) -> None:
    job = jobs.load_job(job_id)
    query = str(job.get("query", "")).strip()
    prompt_id = str(job.get("prompt_id", "")).strip()
    rubric_id = str(job.get("rubric_id", "")).strip()
    samples = max(1, min(int(job.get("samples", 1)), 20))
    state: dict[str, str] = {"run_id": ""}

    try:
        prompt = versions.load_prompt(prompt_id)
        rubric = versions.load_rubric(rubric_id)
    except (FileNotFoundError, ValueError) as exc:
        jobs.finish_job(job_id, error=f"Unknown prompt or rubric version: {exc}")
        return

    case = Case(
        case_id=str(job.get("case_id") or new_id("adhoc")),
        prompt=query,
        tags=["adhoc", "chat"],
    )

    def report_progress(
        phase: RunPhase,
        sample_index: int,
        sample_total: int,
        current_run_id: str,
    ) -> None:
        state["run_id"] = current_run_id
        completed = sample_index if phase == "sample_done" else max(0, sample_index - 1)
        current = sample_index if phase != "prepare" else 0
        _update_progress(
            job_id,
            phase=phase,
            current_sample=current,
            completed_samples=completed,
            run_id=current_run_id,
        )

    try:
        manifest = run_case_samples(
            case,
            prompt.text,
            prompt.prompt_id,
            rubric,
            samples=samples,
            on_progress=report_progress,
        )
        jobs.finish_job(
            job_id,
            result={"run_id": manifest.run_id, "sample_count": manifest.sample_count},
            result_url=f"/runs/{manifest.run_id}",
        )
    except (KeyError, requests.RequestException, RuntimeError, ValueError) as exc:
        error_message = _run_error_message(exc)
        if state["run_id"]:
            jobs.update_job(job_id, run_id=state["run_id"])
        jobs.finish_job(job_id, error=error_message)


def _process_prompt_draft(job_id: str) -> None:
    job = jobs.load_job(job_id)
    base_id = str(job.get("base_id", "")).strip()
    review_ids = list(job.get("review_ids") or [])
    try:
        draft = versions.draft_prompt(base_id, review_ids)
        jobs.finish_job(
            job_id,
            result=draft,
            result_url=f"/versions/prompts/draft/{job_id}",
        )
    except Exception as exc:
        jobs.finish_job(job_id, error=str(exc))


def _process_rubric_draft(job_id: str) -> None:
    job = jobs.load_job(job_id)
    base_id = str(job.get("base_id", "")).strip()
    review_ids = list(job.get("review_ids") or [])
    try:
        draft = versions.draft_rubric(base_id, review_ids)
        jobs.finish_job(
            job_id,
            result=draft,
            result_url=f"/versions/rubrics/draft/{job_id}",
        )
    except Exception as exc:
        jobs.finish_job(job_id, error=str(exc))


_PROCESSORS: dict[str, Callable[[str], None]] = {
    KIND_EXPERIMENT: _process_experiment,
    KIND_PROMPT_DRAFT: _process_prompt_draft,
    KIND_RUBRIC_DRAFT: _process_rubric_draft,
}


def _dispatch(job_id: str) -> None:
    job = jobs.load_job(job_id)
    kind = job.get("kind")
    processor = _PROCESSORS.get(kind)
    if processor is None:
        jobs.finish_job(job_id, error=f"Unknown job kind: {kind!r}")
        return
    processor(job_id)


def _submit(job_id: str) -> None:
    pool = _ensure_executor()
    pool.submit(_dispatch, job_id)


def _ensure_executor() -> ThreadPoolExecutor:
    global _executor
    with _executor_lock:
        if _executor is None:
            _executor = ThreadPoolExecutor(
                max_workers=DEFAULT_MAX_WORKERS,
                thread_name_prefix="harness-queue",
            )
        return _executor


def start_worker(max_workers: int | None = None) -> None:
    """Start the background worker pool (idempotent)."""
    global _executor, DEFAULT_MAX_WORKERS
    if max_workers is not None:
        DEFAULT_MAX_WORKERS = max(1, max_workers)
    _ensure_executor()


def shutdown_worker(wait: bool = True) -> None:
    global _executor
    with _executor_lock:
        if _executor is not None:
            _executor.shutdown(wait=wait, cancel_futures=False)
            _executor = None


def enqueue_experiment(
    *,
    job_id: str,
    query: str,
    prompt_id: str,
    rubric_id: str,
    samples: int = 1,
    case_id: str | None = None,
) -> dict:
    """Queue an ad-hoc query-answer evaluation; rubric is applied on completion."""
    samples = max(1, min(samples, 20))
    payload = jobs.start_job(
        job_id,
        KIND_EXPERIMENT,
        query=query,
        prompt_id=prompt_id,
        rubric_id=rubric_id,
        agent_model=config.agent_model(),
        judge_model=config.judge_model(),
        samples=samples,
        case_id=case_id or new_id("adhoc"),
        phase="queued",
        current_sample=0,
        completed_samples=0,
        message="Queued…",
        run_id="",
    )
    _submit(job_id)
    return payload


def enqueue_prompt_draft(*, job_id: str, base_id: str, review_ids: list[str]) -> dict:
    payload = jobs.start_job(
        job_id,
        KIND_PROMPT_DRAFT,
        base_id=base_id,
        review_ids=review_ids,
        message="Queued…",
    )
    _submit(job_id)
    return payload


def enqueue_rubric_draft(*, job_id: str, base_id: str, review_ids: list[str]) -> dict:
    payload = jobs.start_job(
        job_id,
        KIND_RUBRIC_DRAFT,
        base_id=base_id,
        review_ids=review_ids,
        message="Queued…",
    )
    _submit(job_id)
    return payload


def recover_stale_jobs(max_age_seconds: int = 3600) -> int:
    """Mark long-running jobs as failed (crash recovery). Returns count updated."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    recovered = 0
    for job in jobs.list_jobs():
        if job.get("status") != "running":
            continue
        created = job.get("created_at", "")
        try:
            started = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
        if (now - started).total_seconds() <= max_age_seconds:
            continue
        jobs.finish_job(
            job["job_id"],
            error="Job timed out — worker may have stopped.",
        )
        recovered += 1
    return recovered
