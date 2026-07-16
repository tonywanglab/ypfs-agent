"""Immutable prompt/rubric version storage and AI-assisted draft generation."""

from __future__ import annotations

import json
import re
from pathlib import Path

from . import config, llm, reviews, runner
from .checks import CHECKS_BY_ID
from .models import PromptVersion, Rubric, RubricCriterion, SupervisorReview
from .storage import EVALS_DIR, atomic_write_json, now_iso, read_json

PROMPTS_DIR = EVALS_DIR / "prompts"
RUBRICS_DIR = EVALS_DIR / "rubrics"
_VERSION_RE = re.compile(r"^(prompt|rubric)_v(\d+)$")


def _version(value: str, kind: str) -> int:
    match = _VERSION_RE.fullmatch(value)
    if not match or match.group(1) != kind:
        raise ValueError(f"Invalid {kind} version id: {value!r}")
    return int(match.group(2))


def _path(directory: Path, version_id: str, kind: str) -> Path:
    _version(version_id, kind)
    return directory / f"{version_id}.json"


def list_prompts() -> list[PromptVersion]:
    if not PROMPTS_DIR.exists():
        return []
    prompts = [
        PromptVersion.from_dict(read_json(path))
        for path in PROMPTS_DIR.glob("prompt_v*.json")
    ]
    return sorted(prompts, key=lambda item: item.version)


def list_rubrics() -> list[Rubric]:
    if not RUBRICS_DIR.exists():
        return []
    rubrics = [
        Rubric.from_dict(read_json(path))
        for path in RUBRICS_DIR.glob("rubric_v*.json")
    ]
    return sorted(rubrics, key=lambda item: item.version)


def load_prompt(prompt_id: str) -> PromptVersion:
    return PromptVersion.from_dict(read_json(_path(PROMPTS_DIR, prompt_id, "prompt")))


def load_rubric(rubric_id: str) -> Rubric:
    return Rubric.from_dict(read_json(_path(RUBRICS_DIR, rubric_id, "rubric")))


def latest_prompt() -> PromptVersion:
    prompts = list_prompts()
    if not prompts:
        raise FileNotFoundError("No prompt versions exist")
    return prompts[-1]


def latest_rubric() -> Rubric:
    rubrics = list_rubrics()
    if not rubrics:
        raise FileNotFoundError("No rubric versions exist")
    return rubrics[-1]


def validate_criteria(criteria: list[RubricCriterion]) -> None:
    if not criteria:
        raise ValueError("A rubric must contain at least one criterion")
    seen: set[str] = set()
    for criterion in criteria:
        if not criterion.id or criterion.id in seen:
            raise ValueError(f"Rubric criterion IDs must be non-empty and unique: {criterion.id!r}")
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
        raise llm.LLMError("Rubric draft criteria must be a list")
    criteria = [RubricCriterion.from_dict(item) for item in raw_criteria]
    validate_criteria(criteria)
    return {
        "kind": "rubric",
        "base_id": base_rubric_id,
        "review_ids": review_ids,
        "criteria": [criterion.to_dict() for criterion in criteria],
        "rationale": str(parsed.get("rationale", "")).strip(),
    }


def save_prompt(
    base_prompt_id: str,
    text: str,
    rationale: str,
    review_ids: list[str],
) -> PromptVersion:
    load_prompt(base_prompt_id)
    if not text.strip():
        raise ValueError("Prompt text cannot be empty")
    version = max((prompt.version for prompt in list_prompts()), default=0) + 1
    prompt = PromptVersion(
        prompt_id=f"prompt_v{version}",
        version=version,
        text=text.strip(),
        created_at=now_iso(),
        parent_prompt_id=base_prompt_id,
        rationale=rationale.strip(),
        derived_from_review_ids=review_ids,
    )
    path = _path(PROMPTS_DIR, prompt.prompt_id, "prompt")
    if path.exists():
        raise FileExistsError(f"{prompt.prompt_id} already exists")
    atomic_write_json(path, prompt.to_dict())
    if review_ids:
        reviews.mark_reviews_used(review_ids, prompt.prompt_id)
    return prompt


def save_rubric(
    base_rubric_id: str,
    criteria: list[RubricCriterion],
    rationale: str,
    review_ids: list[str],
) -> Rubric:
    load_rubric(base_rubric_id)
    validate_criteria(criteria)
    version = max((rubric.version for rubric in list_rubrics()), default=0) + 1
    rubric = Rubric(
        rubric_id=f"rubric_v{version}",
        version=version,
        criteria=criteria,
        created_at=now_iso(),
        parent_rubric_id=base_rubric_id,
        rationale=rationale.strip(),
        derived_from_review_ids=review_ids,
    )
    path = _path(RUBRICS_DIR, rubric.rubric_id, "rubric")
    if path.exists():
        raise FileExistsError(f"{rubric.rubric_id} already exists")
    atomic_write_json(path, rubric.to_dict())
    if review_ids:
        reviews.mark_reviews_used(review_ids, rubric.rubric_id)
    return rubric


def available_reviews(target: str) -> list[SupervisorReview]:
    return [
        review
        for review in reviews.list_open_reviews()
        if review.verdict == "unacceptable" and review.failure_attribution == target
    ]


def reconcile_used_reviews() -> None:
    """Backfill status=used for reviews already listed on saved versions."""
    used_by: dict[str, str] = {}
    for prompt in list_prompts():
        for review_id in prompt.derived_from_review_ids:
            used_by[review_id] = prompt.prompt_id
    for rubric in list_rubrics():
        for review_id in rubric.derived_from_review_ids:
            used_by[review_id] = rubric.rubric_id
    for review_id, version_id in used_by.items():
        reviews.mark_review_used(review_id, version_id)
