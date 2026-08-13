"""Safe, atomic file storage for the evaluation harness.

All harness state lives under EVALS_DIR. Every relative path is resolved and
checked against its base directory before any read/write, mirroring the
traversal guard in agent/tools.py's `_safe_id`. Writes are atomic (write to a
temp file in the same directory, then os.replace) so a crash mid-write never
leaves a corrupt JSON/JSONL file behind.
"""

from __future__ import annotations

import json
import os
import secrets
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_DIR = REPO_ROOT / "evals"


def now_iso() -> str:
    """UTC timestamp, second precision, ISO-8601 with a trailing Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(6)}"


def safe_path(*parts: str, base: Path = EVALS_DIR) -> Path:
    """Resolve parts under base, rejecting traversal outside it."""
    resolved = (base / Path(*parts)).resolve()
    base_resolved = base.resolve()
    if not resolved.is_relative_to(base_resolved):
        raise ValueError(f"Invalid path outside {base}: {parts!r}")
    return resolved


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def atomic_write_json(path: Path, data) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, default=str) + "\n")


def read_json(path: Path):
    return json.loads(path.read_text())


def read_json_default(path: Path, default):
    return read_json(path) if path.exists() else default


def append_jsonl(path: Path, record: dict) -> None:
    """Append one record. Not safe for concurrent writers, which is fine for
    a single local supervisor process."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def rewrite_jsonl(path: Path, records: list[dict]) -> None:
    """Atomically replace the full contents of a jsonl file (e.g. updating one
    row's field in place)."""
    text = "".join(json.dumps(r, default=str) + "\n" for r in records)
    atomic_write_text(path, text)
