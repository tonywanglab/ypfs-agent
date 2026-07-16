import pytest

from harness import llm, reviews, versions
from harness.models import PromptVersion, Rubric, RubricCriterion
from harness.storage import atomic_write_json


def _seed_versions():
    prompt = PromptVersion("prompt_v1", 1, "base prompt", "t")
    rubric = Rubric(
        "rubric_v1",
        1,
        [RubricCriterion("quality", "good answer", "llm")],
        "t",
    )
    atomic_write_json(versions.PROMPTS_DIR / "prompt_v1.json", prompt.to_dict())
    atomic_write_json(versions.RUBRICS_DIR / "rubric_v1.json", rubric.to_dict())
    return prompt, rubric


def test_immutable_prompt_save_uses_next_version(evals_dir):
    _seed_versions()
    review = reviews.create_review("run_1", "unacceptable", "too vague", "prompt_issue")
    saved = versions.save_prompt("prompt_v1", "new prompt", "why", [review.review_id])
    assert saved.prompt_id == "prompt_v2"
    assert versions.load_prompt("prompt_v1").text == "base prompt"
    assert versions.load_prompt("prompt_v2").text == "new prompt"
    used = reviews.load_review(review.review_id)
    assert used.status == "used"
    assert used.used_by_version_id == "prompt_v2"
    assert versions.available_reviews("prompt_issue") == []


def test_prompt_draft_is_not_persisted_until_save(evals_dir, monkeypatch):
    _seed_versions()
    review = reviews.create_review("missing_run", "unacceptable", "too vague", "prompt_issue")
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "draft prompt",
        "rationale": "address feedback",
    })
    draft = versions.draft_prompt("prompt_v1", [review.review_id])
    assert draft["prompt_text"] == "draft prompt"
    assert [item.prompt_id for item in versions.list_prompts()] == ["prompt_v1"]


def test_rubric_draft_validates_and_save_is_explicit(evals_dir, monkeypatch):
    _seed_versions()
    review = reviews.create_review("missing_run", "unacceptable", "missing test", "rubric_issue")
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "criteria": [
            {"id": "quality", "description": "good answer", "check_type": "llm"},
            {"id": "depth", "description": "deep answer", "check_type": "llm"},
        ],
        "rationale": "add depth",
    })
    draft = versions.draft_rubric("rubric_v1", [review.review_id])
    assert len(versions.list_rubrics()) == 1
    saved = versions.save_rubric(
        "rubric_v1",
        [RubricCriterion.from_dict(item) for item in draft["criteria"]],
        draft["rationale"],
        draft["review_ids"],
    )
    assert saved.rubric_id == "rubric_v2"
    assert reviews.load_review(review.review_id).status == "used"
    assert versions.available_reviews("rubric_issue") == []


def test_invalid_deterministic_check_is_rejected():
    with pytest.raises(ValueError):
        versions.validate_criteria([
            RubricCriterion("x", "x", "deterministic", deterministic_check="missing")
        ])
