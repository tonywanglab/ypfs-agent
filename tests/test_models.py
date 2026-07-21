from harness.models import Case, Feedback, PromptVersion, RunManifest


def test_version_and_run_contracts_roundtrip():
    prompt = PromptVersion("prompt_v1", 1, "text", "t")
    manifest = RunManifest(
        "run_1",
        "case_1",
        "anthropic/claude-fable-5",
        prompt.prompt_id,
        "t",
    )
    assert PromptVersion.from_dict(prompt.to_dict()) == prompt
    assert RunManifest.from_dict(manifest.to_dict()) == manifest


def test_run_manifest_migrates_legacy_judged_status():
    migrated = RunManifest.from_dict({
        "run_id": "run_1",
        "case_id": "case_1",
        "model": "anthropic/claude-fable-5",
        "prompt_id": "prompt_v1",
        "created_at": "t",
        "status": "judged",
    })
    assert migrated.status == "complete"
    assert migrated.agent_model == "anthropic/claude-fable-5"


def test_feedback_roundtrip():
    feedback = Feedback("fb_1", "run_1", 1, "highlighted text", "should be clearer", "t")
    assert Feedback.from_dict(feedback.to_dict()) == feedback


def test_case_roundtrip():
    case = Case("case_1", "question", ["plan"], "notes")
    assert Case.from_dict(case.to_dict()) == case
