"""Persisted evaluation jobs — single source of truth for queue state.

The web layer reads public_status_payload() only; full job records may hold
pipeline inputs (query, prompt_id, etc.) but never duplicate run artifacts.
"""

from __future__ import annotations

import re
from typing import Any

from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json

JOBS_DIR = EVALS_DIR / "jobs"
_JOB_ID_RE = re.compile(r"^job_[0-9a-f]{12}$")

KIND_EXPERIMENT = "experiment"
KIND_PROMPT_DRAFT = "prompt_draft"
KIND_RUBRIC_DRAFT = "rubric_draft"

# Fields exposed to the web/UI — pipeline internals stay server-side only.
_PUBLIC_FIELDS = frozenset({
    "job_id",
    "kind",
    "status",
    "error",
    "result_url",
    "phase",
    "current_sample",
    "completed_samples",
    "samples",
    "message",
    "run_id",
})


def new_job_id() -> str:
    return new_id("job")


def is_job_id(job_id: str) -> bool:
    return bool(_JOB_ID_RE.fullmatch(job_id or ""))


def _path(job_id: str):
    return JOBS_DIR / f"{job_id}.json"


def list_jobs() -> list[dict]:
    if not JOBS_DIR.exists():
        return []
    out = []
    for path in sorted(JOBS_DIR.glob("job_*.json")):
        out.append(read_json(path))
    return out


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
    fields: dict[str, Any] = {
        "status": status,
        "result": result,
        "result_url": result_url,
        "error": error,
        "finished_at": now_iso(),
    }
    if status == "finished":
        fields["message"] = "Complete."
    return update_job(job_id, **fields)


def public_status_payload(job_id: str) -> dict:
    """Trimmed view for the web — no query text, review ids, or draft payloads."""
    job = load_job(job_id)
    payload = {key: job.get(key) for key in _PUBLIC_FIELDS if key in job}
    payload.setdefault("job_id", job_id)
    payload.setdefault("status", "finished")
    payload.setdefault("kind", job.get("kind"))
    if job.get("status") == "finished" and job.get("run_id") and not payload.get("result_url"):
        payload["result_url"] = f"/runs/{job['run_id']}"
    return payload
