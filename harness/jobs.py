"""Persisted long-running UI jobs (draft generation, etc.).

Experiment tracking lives under evals/experiments/; draft jobs use this
module so the client can poll a single ActiveJob contract.
"""

from __future__ import annotations

import re
from typing import Any

from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json

JOBS_DIR = EVALS_DIR / "jobs"
_JOB_ID_RE = re.compile(r"^job_[0-9a-f]{12}$")

KIND_PROMPT_DRAFT = "prompt_draft"
KIND_RUBRIC_DRAFT = "rubric_draft"


def new_job_id() -> str:
    return new_id("job")


def is_job_id(job_id: str) -> bool:
    return bool(_JOB_ID_RE.fullmatch(job_id or ""))


def _path(job_id: str):
    return JOBS_DIR / f"{job_id}.json"


def start_job(job_id: str, kind: str, **extra: Any) -> dict:
    if not is_job_id(job_id):
        raise ValueError(f"Invalid job id: {job_id!r}")
    payload = {
        "job_id": job_id,
        "kind": kind,
        "status": "running",
        "created_at": now_iso(),
        "error": None,
        "result_url": None,
        "result": None,
        **extra,
    }
    atomic_write_json(_path(job_id), payload)
    return payload


def load_job(job_id: str) -> dict:
    return read_json(_path(job_id))


def update_job(job_id: str, **fields: Any) -> dict:
    payload = load_job(job_id)
    payload.update(fields)
    atomic_write_json(_path(job_id), payload)
    return payload


def finish_job(
    job_id: str,
    *,
    result: dict | None = None,
    result_url: str | None = None,
    error: str | None = None,
) -> dict:
    status = "failed" if error else "finished"
    return update_job(
        job_id,
        status=status,
        result=result,
        result_url=result_url,
        error=error,
        finished_at=now_iso(),
    )


def job_status_payload(job_id: str) -> dict:
    job = load_job(job_id)
    return {
        "job_id": job.get("job_id", job_id),
        "kind": job.get("kind"),
        "status": job.get("status", "finished"),
        "error": job.get("error"),
        "result_url": job.get("result_url"),
    }
