"""Active-version pointers and the one-branch-per-cycle lock.

Persisted to evals/registry.json. This is the single source of truth for
which rubric and prompt version are "active" (used for incumbent runs), and
enforces the harness's core safety rule: a review cycle may move exactly one
branch (rubric or prompt) toward approval at a time. If a review implicates
the other branch while one is already open, the request is queued rather
than rejected outright.
"""

from __future__ import annotations

import fcntl
import threading
from collections.abc import Callable
from typing import Literal

from .storage import EVALS_DIR, atomic_write_json, now_iso, read_json_default

REGISTRY_PATH = EVALS_DIR / "registry.json"

Branch = Literal["rubric", "prompt"]
_THREAD_LOCK = threading.RLock()


class CycleLockedError(Exception):
    """Raised when a proposal of the other branch type is already open."""

    def __init__(self, locked_branch: Branch):
        self.locked_branch = locked_branch
        super().__init__(
            f"A {locked_branch} review cycle is already open; this request "
            "has been queued for the next cycle."
        )


def _default_registry() -> dict:
    return {
        "active_rubric_id": "rubric_v1",
        "active_prompt_id": "prompt_v1",
        "cycle": {"locked_branch": None, "opened_at": None, "opened_by": None},
        "pending_queue": {"rubric": [], "prompt": []},
        "history": [],
    }


def _load_unlocked() -> dict:
    data = read_json_default(REGISTRY_PATH, None)
    if data is None:
        data = _default_registry()
        atomic_write_json(REGISTRY_PATH, data)
    # Backfill keys for registries written by an older harness version.
    data.setdefault("pending_queue", {"rubric": [], "prompt": []})
    data.setdefault("history", [])
    data.setdefault("cycle", {"locked_branch": None, "opened_at": None, "opened_by": None})
    return data


def _locked_update(change: Callable[[dict], None]) -> dict:
    """Serialize a registry read-modify-write across threads and processes."""
    with _THREAD_LOCK:
        lock_path = REGISTRY_PATH.with_suffix(f"{REGISTRY_PATH.suffix}.lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                data = _load_unlocked()
                change(data)
                atomic_write_json(REGISTRY_PATH, data)
                return data
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def load() -> dict:
    with _THREAD_LOCK:
        return _load_unlocked()


def save(data: dict) -> None:
    with _THREAD_LOCK:
        atomic_write_json(REGISTRY_PATH, data)


def active_rubric_id() -> str:
    return load()["active_rubric_id"]


def active_prompt_id() -> str:
    return load()["active_prompt_id"]


def locked_branch() -> Branch | None:
    return load()["cycle"]["locked_branch"]


def lock_cycle(branch: Branch, opened_by: str = "system") -> dict:
    """Open (or continue) a review cycle on `branch`.

    Raises CycleLockedError if the other branch is already open. Idempotent
    if the same branch is already locked.
    """
    data, _ = open_cycle(branch, opened_by=opened_by)
    return data


def open_cycle(branch: Branch, opened_by: str = "system") -> tuple[dict, bool]:
    """Open a cycle and report whether this call created the lock."""
    opened = False

    def change(data: dict) -> None:
        nonlocal opened
        current = data["cycle"]["locked_branch"]
        if current is not None and current != branch:
            raise CycleLockedError(current)
        if current is None:
            data["cycle"] = {
                "locked_branch": branch,
                "opened_at": now_iso(),
                "opened_by": opened_by,
            }
            opened = True

    return _locked_update(change), opened


def enqueue(branch: Branch, ref_id: str) -> None:
    """Record a deferred request (e.g. a review implicating `branch`) so it
    can be actioned once the current cycle closes."""
    def change(data: dict) -> None:
        queue = data["pending_queue"].setdefault(branch, [])
        if ref_id not in queue:
            queue.append(ref_id)

    _locked_update(change)


def dequeue(branch: Branch, ref_id: str) -> None:
    def change(data: dict) -> None:
        queue = data["pending_queue"].get(branch, [])
        if ref_id in queue:
            queue.remove(ref_id)

    _locked_update(change)


def pending_queue() -> dict:
    return load()["pending_queue"]


def require_cycle(branch: Branch) -> dict:
    data = load()
    current = data["cycle"]["locked_branch"]
    if current != branch:
        raise ValueError(
            f"Cannot decide {branch} artifact while cycle is locked to {current!r}"
        )
    return data


def close_cycle(decision: str, *, expected_branch: Branch | None = None) -> dict:
    """Close the current cycle after an approve/reject decision, archive it
    to history, and unlock so the other branch may proceed."""
    def change(data: dict) -> None:
        cycle = data["cycle"]
        current = cycle["locked_branch"]
        if expected_branch is not None and current != expected_branch:
            raise ValueError(
                f"Cannot close {expected_branch} cycle while locked to {current!r}"
            )
        if current is not None:
            data["history"].append({**cycle, "closed_at": now_iso(), "decision": decision})
        data["cycle"] = {"locked_branch": None, "opened_at": None, "opened_by": None}

    return _locked_update(change)


def set_active_rubric(rubric_id: str) -> None:
    _locked_update(lambda data: data.__setitem__("active_rubric_id", rubric_id))


def set_active_prompt(prompt_id: str) -> None:
    _locked_update(lambda data: data.__setitem__("active_prompt_id", prompt_id))
