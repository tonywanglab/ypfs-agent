"""Immutable prompt version storage (Postgres) and AI-assisted drafts."""

from __future__ import annotations

import json
import re

from . import config, dbio, feedback, llm, runner
from .models import PromptVersion
from .storage import now_iso

_VERSION_RE = re.compile(r"^prompt_v(\d+)$")


def _version(value: str) -> int:
    match = _VERSION_RE.fullmatch(value)
    if not match:
        raise ValueError(f"Invalid prompt version id: {value!r}")
    return int(match.group(1))


def _prompt_from_row(row: dict) -> PromptVersion:
    return PromptVersion(
        prompt_id=row["prompt_id"],
        version=row["version"],
        text=row["text"],
        created_at=row["created_at"],
        parent_prompt_id=row["parent_prompt_id"],
        rationale=row["rationale"] or "",
    )


def list_prompts() -> list[PromptVersion]:
    rows = dbio.q("SELECT * FROM prompt_versions ORDER BY version")
    return [_prompt_from_row(row) for row in rows]


def load_prompt(prompt_id: str) -> PromptVersion:
    _version(prompt_id)
    row = dbio.q1("SELECT * FROM prompt_versions WHERE prompt_id = %s", (prompt_id,))
    if row is None:
        raise FileNotFoundError(f"Prompt version {prompt_id!r} does not exist")
    return _prompt_from_row(row)


def latest_prompt_id() -> str:
    """The current prompt_id only — cheap, for callers (e.g. the header chip
    on every page) that don't need the full version."""
    row = dbio.q1("SELECT prompt_id FROM prompt_versions ORDER BY version DESC LIMIT 1")
    if row is None:
        raise FileNotFoundError("No prompt versions exist")
    return row["prompt_id"]


def latest_prompt() -> PromptVersion:
    return load_prompt(latest_prompt_id())


def _feedback_context(feedback_ids: list[str]) -> list[dict]:
    if not feedback_ids:
        raise ValueError("Select at least one feedback item")
    bundles: dict[str, dict] = {}
    context = []
    for feedback_id in feedback_ids:
        item = feedback.load_feedback(feedback_id)
        if item.run_id not in bundles:
            try:
                bundles[item.run_id] = runner.load_run_bundle(item.run_id)
            except FileNotFoundError:
                bundles[item.run_id] = None
        bundle = bundles[item.run_id]
        if bundle is None:
            context.append({
                "selected_text": item.selected_text,
                "comment": item.comment,
                "sample_index": item.sample_index,
                "run": {"unavailable": True},
            })
            continue
        sample = next(
            (s for s in bundle["samples"] if s["index"] == item.sample_index),
            bundle["samples"][0],
        )
        context.append({
            "question": bundle["case"]["prompt"],
            "sample_index": item.sample_index,
            "answer": sample["answer"],
            "selected_text": item.selected_text,
            "comment": item.comment,
        })
    return context


def draft_prompt(base_prompt_id: str, feedback_ids: list[str]) -> dict:
    base = load_prompt(base_prompt_id)
    context = _feedback_context(feedback_ids)
    parsed = llm.chat_json(
        system_prompt=(
            "You edit a financial-crisis research agent system prompt. Revise the "
            "chosen base prompt only where the highlighted excerpts and supervisor "
            "comments demonstrate a prompt failure. Preserve useful constraints and "
            "do not encode case-specific answers. Return JSON with prompt_text and "
            "rationale."
        ),
        user_prompt=json.dumps(
            {"base_prompt": base.to_dict(), "supervisor_feedback": context},
            indent=2,
            default=str,
        ),
        model=config.editor_model(),
    )
    prompt_text = str(parsed.get("prompt_text", "")).strip()
    if not prompt_text:
        raise llm.LLMError("Prompt draft did not contain prompt_text")
    return {
        "kind": "prompt",
        "base_id": base_prompt_id,
        "feedback_ids": feedback_ids,
        "prompt_text": prompt_text,
        "rationale": str(parsed.get("rationale", "")).strip(),
    }


def _unique_violation():
    from psycopg.errors import UniqueViolation
    return UniqueViolation


def save_prompt(base_prompt_id: str, text: str, rationale: str) -> PromptVersion:
    load_prompt(base_prompt_id)
    if not text.strip():
        raise ValueError("Prompt text cannot be empty")
    # UNIQUE(version) turns a concurrent double-allocation into a retry.
    for attempt in (0, 1):
        try:
            with dbio.transaction():
                row = dbio.q1(
                    """
                    WITH next AS (
                        SELECT coalesce(max(version), 0) + 1 AS v FROM prompt_versions
                    )
                    INSERT INTO prompt_versions
                        (prompt_id, version, text, created_at, parent_prompt_id, rationale)
                    SELECT 'prompt_v' || v, v, %s, %s, %s, %s FROM next
                    RETURNING prompt_id, version
                    """,
                    (text.strip(), now_iso(), base_prompt_id, rationale.strip()),
                )
            break
        except _unique_violation():
            if attempt:
                raise FileExistsError("Prompt version allocation raced twice; retry")
    return load_prompt(row["prompt_id"])
