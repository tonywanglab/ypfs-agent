import time

import pytest

from harness import config, evaluator, jobs, queue, seed, versions
from harness.models import Case, CriterionVerdict, Judgment, Rubric, RubricCriterion


def _sync_submit(monkeypatch):
    """Run queued jobs inline so tests don't depend on thread timing."""
    monkeypatch.setattr(queue, "_submit", lambda job_id: queue._dispatch(job_id))


def _patch_pipeline(monkeypatch, answer="answer"):
    calls = {"n": 0}

    def fake_agent_run(user_msg, history, model, system_prompt):
        calls["n"] += 1
        return f"{answer}-{calls['n']}", []

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

    monkeypatch.setattr("harness.runner.agent_run", fake_agent_run)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)


def test_enqueue_experiment_runs_pipeline(evals_dir, monkeypatch):
    seed.seed_all()
    _sync_submit(monkeypatch)
    _patch_pipeline(monkeypatch)

    job_id = jobs.new_job_id()
    queue.enqueue_experiment(
        job_id=job_id,
        query="question",
        prompt_id="prompt_v1",
        rubric_id="rubric_v1",
        samples=2,
    )
    job = jobs.load_job(job_id)
    assert job["status"] == "finished"
    assert job["run_id"]
    assert job["result"]["sample_count"] == 2


def test_public_status_hides_pipeline_inputs(evals_dir, monkeypatch):
    seed.seed_all()
    _sync_submit(monkeypatch)
    _patch_pipeline(monkeypatch)

    job_id = jobs.new_job_id()
    queue.enqueue_experiment(
        job_id=job_id,
        query="secret query text",
        prompt_id="prompt_v1",
        rubric_id="rubric_v1",
    )
    public = jobs.public_status_payload(job_id)
    assert "query" not in public
    assert "secret query text" not in str(public)
    assert public["status"] == "finished"
    assert public["run_id"]


def test_concurrent_jobs(evals_dir, monkeypatch):
    seed.seed_all()
    monkeypatch.setattr(queue, "DEFAULT_MAX_WORKERS", 2)
    queue.shutdown_worker(wait=True)
    queue.start_worker(max_workers=2)

    delays = {"n": 0}

    def slow_agent_run(user_msg, history, model, system_prompt):
        delays["n"] += 1
        time.sleep(0.05)
        return f"answer-{delays['n']}", []

    def fake_judge_answer(**kwargs):
        return Judgment(
            "judg_1",
            kwargs["run_id"],
            config.judge_model(),
            [CriterionVerdict("quality", "pass", "good")],
            "ok",
            "",
            "t",
        )

    monkeypatch.setattr("harness.runner.agent_run", slow_agent_run)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)

    ids = [jobs.new_job_id(), jobs.new_job_id()]
    for job_id in ids:
        queue.enqueue_experiment(
            job_id=job_id,
            query="q",
            prompt_id="prompt_v1",
            rubric_id="rubric_v1",
        )

    deadline = time.time() + 5
    while time.time() < deadline:
        if all(jobs.load_job(jid)["status"] == "finished" for jid in ids):
            break
        time.sleep(0.05)
    else:
        pytest.fail("Concurrent jobs did not finish in time")

    assert jobs.load_job(ids[0])["run_id"] != jobs.load_job(ids[1])["run_id"]


def test_failed_job_preserves_partial_run_id(evals_dir, monkeypatch):
    seed.seed_all()
    _sync_submit(monkeypatch)

    calls = {"n": 0}

    def flaky_agent(user_msg, history, model, system_prompt):
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("agent blew up")
        return "ok", []

    def fake_judge(**kwargs):
        return Judgment(
            "judg_1",
            kwargs["run_id"],
            config.judge_model(),
            [CriterionVerdict("quality", "pass", "good")],
            "ok",
            "",
            "t",
        )

    monkeypatch.setattr("harness.runner.agent_run", flaky_agent)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge)

    job_id = jobs.new_job_id()
    queue.enqueue_experiment(
        job_id=job_id,
        query="q",
        prompt_id="prompt_v1",
        rubric_id="rubric_v1",
        samples=2,
    )
    job = jobs.load_job(job_id)
    assert job["status"] == "failed"
    assert job["run_id"]  # partial run from sample 1


def test_progress_message_multi_sample():
    assert queue._progress_message(
        "checks",
        current_sample=2,
        completed_samples=1,
        samples=5,
    ) == "Sample 2 of 5 — Running deterministic checks…"
