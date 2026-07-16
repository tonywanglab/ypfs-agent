from harness import config, evaluator, runner
from harness.models import Case, CriterionVerdict, Judgment, Rubric, RubricCriterion


def _rubric():
    return Rubric(
        "rubric_v1",
        1,
        [RubricCriterion("quality", "good", "llm")],
        "t",
    )


def _patch_pipeline(monkeypatch, answer="answer"):
    captured = {"calls": 0}

    def fake_agent_run(user_msg, history, model, system_prompt):
        captured["calls"] += 1
        captured.update(
            user_msg=user_msg,
            history=history,
            model=model,
            system_prompt=system_prompt,
        )
        return (
            f"{answer}-{captured['calls']}" if answer == "answer" else answer
        ), []

    def fake_judge_answer(**kwargs):
        return Judgment(
            f"judg_{captured['calls']}",
            kwargs["run_id"],
            config.judge_model(),
            [CriterionVerdict("quality", "pass", "good")],
            "ok",
            "",
            "t",
        )

    monkeypatch.setattr(runner, "agent_run", fake_agent_run)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)
    return captured


def test_run_case_persists_samples_layout(evals_dir, monkeypatch):
    captured = _patch_pipeline(monkeypatch)
    manifest = runner.run_case(
        Case("case_1", "question"),
        "selected system prompt",
        "prompt_v1",
        _rubric(),
    )
    assert captured["history"] is None
    assert captured["model"] == config.agent_model()
    assert captured["system_prompt"] == "selected system prompt"
    assert manifest.agent_model == config.agent_model()
    assert manifest.judge_model == config.judge_model()
    assert manifest.sample_count == 1

    run_dir = runner.RUNS_DIR / manifest.run_id
    assert {path.name for path in run_dir.iterdir()} == {"case.json", "manifest.json", "samples"}
    sample_dir = run_dir / "samples" / "01"
    assert {path.name for path in sample_dir.iterdir()} == {
        "answer.json",
        "trace.json",
        "checks.json",
        "judgment.json",
    }
    bundle = runner.load_run_bundle(manifest.run_id)
    assert len(bundle["samples"]) == 1
    assert bundle["answer"] == "answer-1"
    assert "checklist" not in bundle


def test_run_case_samples_writes_multiple_samples(evals_dir, monkeypatch):
    _patch_pipeline(monkeypatch)
    manifest = runner.run_case_samples(
        Case("case_1", "question"),
        "prompt",
        "prompt_v1",
        _rubric(),
        samples=3,
    )
    assert manifest.sample_count == 3
    bundle = runner.load_run_bundle(manifest.run_id)
    assert len(bundle["samples"]) == 3
    assert [sample["index"] for sample in bundle["samples"]] == [1, 2, 3]
    assert bundle["samples"][0]["answer"] == "answer-1"
    assert bundle["samples"][2]["answer"] == "answer-3"


def test_load_run_bundle_supports_legacy_flat_layout(evals_dir, monkeypatch):
    from harness.storage import atomic_write_json

    _patch_pipeline(monkeypatch)
    manifest = runner.run_case(Case("case_1", "q"), "prompt", "prompt_v1", _rubric())
    run_dir = runner.RUNS_DIR / manifest.run_id
    sample_dir = run_dir / "samples" / "01"
    for name in ("answer.json", "trace.json", "checks.json", "judgment.json"):
        (run_dir / name).write_text((sample_dir / name).read_text())
    shutil = __import__("shutil")
    shutil.rmtree(sample_dir.parent)

    bundle = runner.load_run_bundle(manifest.run_id)
    assert len(bundle["samples"]) == 1
    assert bundle["samples"][0]["answer"] == "answer-1"


def test_run_case_records_hard_failure(evals_dir, monkeypatch):
    _patch_pipeline(monkeypatch, answer="[stopped: hit MAX_STEPS]")
    manifest = runner.run_case(Case("case_1", "q"), "prompt", "prompt_v1", _rubric())
    assert manifest.hard_failure is True
    bundle = runner.load_run_bundle(manifest.run_id)
    assert bundle["samples"][0]["hard_failure"] is True


def test_run_case_samples_aggregates_hard_failure(evals_dir, monkeypatch):
    calls = {"n": 0}

    def fake_agent_run(user_msg, history, model, system_prompt):
        calls["n"] += 1
        answer = "[stopped: hit MAX_STEPS]" if calls["n"] == 2 else "ok"
        return answer, []

    def fake_judge_answer(**kwargs):
        return Judgment(
            f"judg_{calls['n']}",
            kwargs["run_id"],
            config.judge_model(),
            [CriterionVerdict("quality", "pass", "good")],
            "ok",
            "",
            "t",
        )

    monkeypatch.setattr(runner, "agent_run", fake_agent_run)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)
    manifest = runner.run_case_samples(
        Case("case_1", "q"),
        "prompt",
        "prompt_v1",
        _rubric(),
        samples=2,
    )
    assert manifest.hard_failure is True
    bundle = runner.load_run_bundle(manifest.run_id)
    assert bundle["samples"][0]["hard_failure"] is False
    assert bundle["samples"][1]["hard_failure"] is True


def test_run_case_samples_reports_progress(evals_dir, monkeypatch):
    _patch_pipeline(monkeypatch)
    seen = []

    def on_progress(phase, sample_index, sample_total, run_id):
        seen.append((phase, sample_index, sample_total, run_id))

    manifest = runner.run_case_samples(
        Case("case_1", "question"),
        "prompt",
        "prompt_v1",
        _rubric(),
        samples=2,
        on_progress=on_progress,
    )
    assert manifest.sample_count == 2
    assert seen[0][0] == "prepare"
    assert seen[0][3] == manifest.run_id
    sample_one = [item for item in seen if item[1] == 1]
    assert [phase for phase, *_rest in sample_one] == [
        "agent", "checks", "judge", "sample_done",
    ]
    sample_two = [item for item in seen if item[1] == 2]
    assert [phase for phase, *_rest in sample_two] == [
        "agent", "checks", "judge", "sample_done",
    ]


def test_delete_run_removes_artifacts(evals_dir, monkeypatch):
    _patch_pipeline(monkeypatch)
    manifest = runner.run_case(Case("case_1", "q"), "prompt", "prompt_v1", _rubric())
    runner.delete_run(manifest.run_id)
    assert not (runner.RUNS_DIR / manifest.run_id).exists()
