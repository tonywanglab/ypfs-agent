"""Immutable prompt/rubric version storage (Postgres) and AI-assisted drafts."""

from __future__ import annotations

import json
import re

from . import config, dbio, llm, reviews, runner
from .checks import CHECKS_BY_ID
from .models import PromptVersion, RubricVersion, RubricCriterion, SupervisorReview
from .storage import now_iso

_VERSION_RE = re.compile(r"^(prompt|rubric)_v(\d+)$")


def _version(value: str, kind: str) -> int:
    match = _VERSION_RE.fullmatch(value)
    if not match or match.group(1) != kind:
        raise ValueError(f"Invalid {kind} version id: {value!r}")
    return int(match.group(2))


def _prompt_from_row(row: dict) -> PromptVersion:
    return PromptVersion(
        prompt_id=row["prompt_id"],
        version=row["version"],
        text=row["text"],
        created_at=row["created_at"],
        parent_prompt_id=row["parent_prompt_id"],
        rationale=row["rationale"] or "",
        derived_from_review_ids=row["review_ids"] or [],
    )


def _rubric_from_row(row: dict) -> RubricVersion:
    return RubricVersion(
        rubric_id=row["rubric_id"],
        version=row["version"],
        criteria=[RubricCriterion.from_dict(c) for c in row["criteria"]],
        created_at=row["created_at"],
        parent_rubric_id=row["parent_rubric_id"],
        rationale=row["rationale"] or "",
        derived_from_review_ids=row["review_ids"] or [],
    )


# derived_from_review_ids is folded into the main SELECT via a correlated
# subquery so listing/loading a version never costs a second round trip to
# version_reviews — with the DB on the far side of a network hop, every
# extra query is real, felt latency.
_PROMPT_SELECT = """
    SELECT pv.*, ARRAY(
        SELECT review_id FROM version_reviews
         WHERE version_id = pv.prompt_id ORDER BY review_id
    ) AS review_ids
    FROM prompt_versions pv
"""

_RUBRIC_SELECT = """
    SELECT rv.*, ARRAY(
        SELECT review_id FROM version_reviews
         WHERE version_id = rv.rubric_id ORDER BY review_id
    ) AS review_ids
    FROM rubric_versions rv
"""


def list_prompts() -> list[PromptVersion]:
    rows = dbio.q(_PROMPT_SELECT + " ORDER BY pv.version")
    return [_prompt_from_row(row) for row in rows]


def list_rubrics() -> list[RubricVersion]:
    rows = dbio.q(_RUBRIC_SELECT + " ORDER BY rv.version")
    return [_rubric_from_row(row) for row in rows]


def load_prompt(prompt_id: str) -> PromptVersion:
    _version(prompt_id, "prompt")
    row = dbio.q1(_PROMPT_SELECT + " WHERE pv.prompt_id = %s", (prompt_id,))
    if row is None:
        raise FileNotFoundError(f"Prompt version {prompt_id!r} does not exist")
    return _prompt_from_row(row)


def load_rubric(rubric_id: str) -> RubricVersion:
    _version(rubric_id, "rubric")
    row = dbio.q1(_RUBRIC_SELECT + " WHERE rv.rubric_id = %s", (rubric_id,))
    if row is None:
        raise FileNotFoundError(f"Rubric version {rubric_id!r} does not exist")
    return _rubric_from_row(row)


def latest_prompt_id() -> str:
    """The current prompt_id only — cheap, for callers (e.g. the header chip
    on every page) that don't need the full version + its review links."""
    row = dbio.q1("SELECT prompt_id FROM prompt_versions ORDER BY version DESC LIMIT 1")
    if row is None:
        raise FileNotFoundError("No prompt versions exist")
    return row["prompt_id"]


def latest_rubric_id() -> str:
    row = dbio.q1("SELECT rubric_id FROM rubric_versions ORDER BY version DESC LIMIT 1")
    if row is None:
        raise FileNotFoundError("No rubric versions exist")
    return row["rubric_id"]


def latest_prompt() -> PromptVersion:
    return load_prompt(latest_prompt_id())


def latest_rubric() -> RubricVersion:
    return load_rubric(latest_rubric_id())


def validate_criteria(criteria: list[RubricCriterion]) -> None:
    if not criteria:
        raise ValueError("A rubric must contain at least one criterion")
    seen: set[str] = set()
    for criterion in criteria:
        if not criterion.id or criterion.id in seen:
            raise ValueError(f"RubricVersion criterion IDs must be non-empty and unique: {criterion.id!r}")
        seen.add(criterion.id)
        if not criterion.description.strip():
            raise ValueError(f"Criterion {criterion.id!r} needs a description")
        if criterion.check_type not in ("deterministic", "llm"):
            raise ValueError(f"Invalid check_type for {criterion.id!r}")
        if criterion.weight <= 0:
            raise ValueError(f"Criterion {criterion.id!r} weight must be positive")
        if criterion.check_type == "deterministic":
            if criterion.deterministic_check not in CHECKS_BY_ID:
                raise ValueError(
                    f"Criterion {criterion.id!r} references an unknown deterministic check"
                )
        elif criterion.deterministic_check is not None:
            raise ValueError(
                f"LLM criterion {criterion.id!r} cannot name a deterministic check"
            )


def _run_context_for_review(bundle: dict) -> dict:
    samples = bundle["samples"]
    question = bundle["case"]["prompt"]
    if len(samples) == 1:
        return {
            "question": question,
            "answer": samples[0]["answer"],
            "judgment": samples[0]["judgment"],
        }
    hard_failures = [sample["index"] for sample in samples if sample.get("hard_failure")]
    judge_failures = [
        sample["index"]
        for sample in samples
        if any(
            criterion.get("verdict") == "fail"
            for criterion in sample.get("judgment", {}).get("criteria", [])
        )
    ]
    representative = next(
        (
            sample
            for sample in samples
            if sample.get("hard_failure")
            or any(
                criterion.get("verdict") == "fail"
                for criterion in sample.get("judgment", {}).get("criteria", [])
            )
        ),
        samples[0],
    )
    return {
        "question": question,
        "sample_count": len(samples),
        "hard_failure_samples": hard_failures,
        "judge_failure_samples": judge_failures,
        "representative_sample": representative["index"],
        "answer": representative["answer"],
        "judgment": representative["judgment"],
    }


def _review_context(review_ids: list[str], target: str) -> list[dict]:
    if not review_ids:
        raise ValueError("Select at least one supervisor review")
    context = []
    for review_id in review_ids:
        review = reviews.load_review(review_id)
        if review.verdict != "unacceptable" or review.failure_attribution != target:
            raise ValueError(f"Review {review_id} is not actionable for {target}")
        item = {"review": review.to_dict()}
        try:
            bundle = runner.load_run_bundle(review.run_id)
            item["run"] = _run_context_for_review(bundle)
        except FileNotFoundError:
            item["run"] = {"unavailable": True}
        context.append(item)
    return context


def draft_prompt(base_prompt_id: str, review_ids: list[str]) -> dict:
    base = load_prompt(base_prompt_id)
    context = _review_context(review_ids, "prompt_issue")
    parsed = llm.chat_json(
        system_prompt=(
            "You edit a financial-crisis research agent system prompt. Revise the "
            "chosen base prompt only where the supervisor feedback demonstrates a "
            "prompt failure. Preserve useful constraints and do not encode case-specific "
            "answers. Return JSON with prompt_text and rationale."
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
        "review_ids": review_ids,
        "prompt_text": prompt_text,
        "rationale": str(parsed.get("rationale", "")).strip(),
    }


def draft_rubric(base_rubric_id: str, review_ids: list[str]) -> dict:
    base = load_rubric(base_rubric_id)
    context = _review_context(review_ids, "rubric_issue")
    parsed = llm.chat_json(
        system_prompt=(
            "You edit an evaluation rubric for a financial-crisis research agent. "
            "Revise the chosen base rubric only where the supervisor feedback shows "
            "that the rubric failed to measure intended quality. Preserve valid "
            "criteria and deterministic checks. Return JSON with criteria and rationale."
        ),
        user_prompt=json.dumps(
            {"base_rubric": base.to_dict(), "supervisor_feedback": context},
            indent=2,
            default=str,
        ),
        model=config.editor_model(),
    )
    raw_criteria = parsed.get("criteria", [])
    if not isinstance(raw_criteria, list):
        raise llm.LLMError("RubricVersion draft criteria must be a list")
    criteria = [RubricCriterion.from_dict(item) for item in raw_criteria]
    validate_criteria(criteria)
    return {
        "kind": "rubric",
        "base_id": base_rubric_id,
        "review_ids": review_ids,
        "criteria": [criterion.to_dict() for criterion in criteria],
        "rationale": str(parsed.get("rationale", "")).strip(),
    }


def _link_reviews(version_id: str, review_ids: list[str]) -> None:
    for review_id in review_ids:
        dbio.execute(
            "INSERT INTO version_reviews (version_id, review_id) VALUES (%s, %s)"
            " ON CONFLICT DO NOTHING",
            (version_id, review_id),
        )


def _unique_violation():
    from psycopg.errors import UniqueViolation
    return UniqueViolation


def save_prompt(
    base_prompt_id: str,
    text: str,
    rationale: str,
    review_ids: list[str],
) -> PromptVersion:
    load_prompt(base_prompt_id)
    if not text.strip():
        raise ValueError("Prompt text cannot be empty")
    # Version allocation, review links, and used-marking commit atomically.
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
                _link_reviews(row["prompt_id"], review_ids)
                if review_ids:
                    reviews.mark_reviews_used(review_ids, row["prompt_id"])
            break
        except _unique_violation():
            if attempt:
                raise FileExistsError("Prompt version allocation raced twice; retry")
    return load_prompt(row["prompt_id"])


def save_rubric(
    base_rubric_id: str,
    criteria: list[RubricCriterion],
    rationale: str,
    review_ids: list[str],
) -> RubricVersion:
    load_rubric(base_rubric_id)
    validate_criteria(criteria)
    for attempt in (0, 1):
        try:
            with dbio.transaction():
                row = dbio.q1(
                    """
                    WITH next AS (
                        SELECT coalesce(max(version), 0) + 1 AS v FROM rubric_versions
                    )
                    INSERT INTO rubric_versions
                        (rubric_id, version, criteria, created_at, parent_rubric_id, rationale)
                    SELECT 'rubric_v' || v, v, %s, %s, %s, %s FROM next
                    RETURNING rubric_id, version
                    """,
                    (dbio.jsonb([c.to_dict() for c in criteria]), now_iso(),
                     base_rubric_id, rationale.strip()),
                )
                _link_reviews(row["rubric_id"], review_ids)
                if review_ids:
                    reviews.mark_reviews_used(review_ids, row["rubric_id"])
            break
        except _unique_violation():
            if attempt:
                raise FileExistsError("Rubric version allocation raced twice; retry")
    return load_rubric(row["rubric_id"])


def available_reviews(
    target: str, open_reviews: list[SupervisorReview] | None = None,
) -> list[SupervisorReview]:
    """Pass open_reviews when the caller already fetched it (e.g. once for
    both prompt_issue and rubric_issue) to avoid a second query."""
    return [
        review
        for review in (reviews.list_open_reviews() if open_reviews is None else open_reviews)
        if review.verdict == "unacceptable" and review.failure_attribution == target
    ]
