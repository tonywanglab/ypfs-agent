import threading

import pytest

from harness import feedback, llm, versions


def _seed_prompt_v1(text="base prompt"):
    from harness import dbio
    from harness.storage import now_iso

    dbio.execute(
        "INSERT INTO prompt_versions (prompt_id, version, text, created_at) VALUES (%s, %s, %s, %s)",
        ("prompt_v1", 1, text, now_iso()),
    )


def test_immutable_prompt_save_uses_next_version(pg):
    _seed_prompt_v1("base prompt")
    saved = versions.save_prompt("prompt_v1", "new prompt", "why")
    assert saved.prompt_id == "prompt_v2"
    assert versions.load_prompt("prompt_v1").text == "base prompt"
    assert versions.load_prompt("prompt_v2").text == "new prompt"


def test_save_prompt_allocates_append_only_max_plus_one(pg):
    _seed_prompt_v1("base prompt")
    versions.save_prompt("prompt_v1", "v2 text", "r1")
    versions.save_prompt("prompt_v2", "v3 text", "r2")
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
            saved = versions.save_prompt("prompt_v1", "concurrent text", "race")
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


def test_prompt_draft_is_not_persisted_until_save(pg, make_run, monkeypatch):
    _seed_prompt_v1("base prompt")
    run_id = make_run(answer="the agent's original answer")
    item = feedback.create_feedback(run_id, 1, "original answer", "too vague")
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "draft prompt",
        "rationale": "address feedback",
    })
    draft = versions.draft_prompt("prompt_v1", [item.feedback_id])
    assert draft["prompt_text"] == "draft prompt"
    assert [item.prompt_id for item in versions.list_prompts()] == ["prompt_v1"]


def test_draft_prompt_requires_at_least_one_feedback_item(pg):
    _seed_prompt_v1("base prompt")
    with pytest.raises(ValueError):
        versions.draft_prompt("prompt_v1", [])


def test_draft_prompt_tolerates_a_run_whose_bundle_cannot_load(pg, make_run, monkeypatch):
    # Simulates a run row that outlived its sample artifacts (defensive path;
    # the schema's ON DELETE CASCADE means a normal delete_run() takes
    # feedback with it, so this can only happen via direct row surgery).
    _seed_prompt_v1("base prompt")
    run_id = make_run()
    item = feedback.create_feedback(run_id, 1, "original answer", "too vague")
    from harness import dbio
    dbio.execute("DELETE FROM run_samples WHERE run_id = %s", (run_id,))

    captured = {}

    def fake_chat_json(**kwargs):
        captured["user_prompt"] = kwargs["user_prompt"]
        return {"prompt_text": "draft prompt", "rationale": "r"}

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)
    versions.draft_prompt("prompt_v1", [item.feedback_id])
    assert "unavailable" in captured["user_prompt"]
