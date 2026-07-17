import threading

import pytest

from harness import llm, reviews, versions
from harness.models import RubricCriterion


def _seed_prompt_v1(text="base prompt"):
    from harness import dbio
    from harness.storage import now_iso

    dbio.execute(
        "INSERT INTO prompt_versions (prompt_id, version, text, created_at) VALUES (%s, %s, %s, %s)",
        ("prompt_v1", 1, text, now_iso()),
    )


def _seed_rubric_v1():
    from harness import dbio
    from harness.storage import now_iso

    dbio.execute(
        "INSERT INTO rubric_versions (rubric_id, version, criteria, created_at) VALUES (%s, %s, %s, %s)",
        ("rubric_v1", 1, dbio.jsonb([RubricCriterion("quality", "good answer", "llm").to_dict()]),
         now_iso()),
    )


def test_immutable_prompt_save_uses_next_version(pg, make_run):
    _seed_prompt_v1("base prompt")
    run_id = make_run()
    review = reviews.create_review(run_id, "unacceptable", "too vague", "prompt_issue")
    saved = versions.save_prompt("prompt_v1", "new prompt", "why", [review.review_id])
    assert saved.prompt_id == "prompt_v2"
    assert saved.derived_from_review_ids == [review.review_id]
    assert versions.load_prompt("prompt_v1").text == "base prompt"
    assert versions.load_prompt("prompt_v2").text == "new prompt"
    used = reviews.load_review(review.review_id)
    assert used.status == "used"
    assert used.used_by_version_id == "prompt_v2"
    assert versions.available_reviews("prompt_issue") == []


def test_save_prompt_allocates_append_only_max_plus_one(pg):
    _seed_prompt_v1("base prompt")
    versions.save_prompt("prompt_v1", "v2 text", "r1", [])
    versions.save_prompt("prompt_v2", "v3 text", "r2", [])
    assert [p.prompt_id for p in versions.list_prompts()] == ["prompt_v1", "prompt_v2", "prompt_v3"]
    assert [p.version for p in versions.list_prompts()] == [1, 2, 3]


def test_concurrent_save_prompt_never_duplicates_version(pg):
    # save_prompt retries a UniqueViolation exactly once (see versions.py),
    # which guarantees correctness (no duplicate version ever lands) for a
    # 2-way race — the realistic case of two supervisors saving at once.
    _seed_prompt_v1("base prompt")
    errors = []
    results = []
    lock = threading.Lock()

    def worker():
        try:
            saved = versions.save_prompt("prompt_v1", "concurrent text", "race", [])
            with lock:
                results.append(saved.version)
        except Exception as exc:  # pragma: no cover - only on unexpected failure
            with lock:
                errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert sorted(results) == [2, 3]
    all_versions = [p.version for p in versions.list_prompts()]
    assert len(all_versions) == len(set(all_versions))


def test_prompt_draft_is_not_persisted_until_save(pg, monkeypatch):
    _seed_prompt_v1("base prompt")
    run_id = "run_missing"
    from harness.models import Case, RunManifest
    from harness.runner import save_manifest
    from harness.seed import insert_case

    insert_case(Case(case_id="c1", prompt="q"))
    _seed_rubric_v1()
    save_manifest(
        RunManifest(run_id, "c1", "m", "m", "prompt_v1", "rubric_v1", "2024-01-01T00:00:00Z",
                    status="pending", sample_count=1),
        case_snapshot={"case_id": "c1", "prompt": "q", "tags": [], "notes": ""},
    )
    review = reviews.create_review(run_id, "unacceptable", "too vague", "prompt_issue")
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "draft prompt",
        "rationale": "address feedback",
    })
    draft = versions.draft_prompt("prompt_v1", [review.review_id])
    assert draft["prompt_text"] == "draft prompt"
    assert [item.prompt_id for item in versions.list_prompts()] == ["prompt_v1"]


def test_rubric_draft_validates_and_save_is_explicit(pg, make_run, monkeypatch):
    _seed_prompt_v1("base prompt")
    _seed_rubric_v1()
    run_id = make_run(rubric_id="rubric_v1")
    review = reviews.create_review(run_id, "unacceptable", "missing test", "rubric_issue")
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
