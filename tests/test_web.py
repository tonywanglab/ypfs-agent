from harness import config, reviews, seed, versions, web
from harness.models import RunManifest
from harness.storage import atomic_write_json


def _client(evals_dir, monkeypatch):
    seed.seed_all()
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    return web.create_app().test_client()


def test_chat_exposes_only_prompt_and_rubric_variables(evals_dir, monkeypatch):
    seed.seed_all()
    versions.save_prompt("prompt_v1", "second", "test", [])
    client = _client(evals_dir, monkeypatch)
    body = client.get("/chat").get_data(as_text=True)
    assert 'name="prompt_id"' in body
    assert 'name="rubric_id"' in body
    assert 'name="model"' not in body
    assert config.agent_model() in body
    assert config.judge_model() in body
    assert 'value="prompt_v2"' in body


def test_chat_submission_uses_selected_pair_and_no_model_input(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    captured = {}

    def fake_run_case_samples(case, prompt_text, prompt_id, rubric, samples=1, on_progress=None):
        captured.update(
            prompt_text=prompt_text,
            prompt_id=prompt_id,
            rubric_id=rubric.rubric_id,
            samples=samples,
            progress=on_progress is not None,
        )
        return RunManifest(
            "run_1",
            case.case_id,
            config.agent_model(),
            config.judge_model(),
            prompt_id,
            rubric.rubric_id,
            "t",
            judgment_id="judg_1",
            status="judged",
            sample_count=samples,
        )

    monkeypatch.setattr(web, "run_case_samples", fake_run_case_samples)
    response = client.post("/chat/run", data={
        "query": "question",
        "prompt_id": "prompt_v1",
        "rubric_id": "rubric_v1",
        "samples": "3",
        "experiment_id": "experiment_abcdef123456",
        "model": "malicious/override",
    })
    assert response.status_code == 302
    assert captured["prompt_id"] == "prompt_v1"
    assert captured["rubric_id"] == "rubric_v1"
    assert captured["samples"] == 3
    assert captured["progress"] is True
    assert "/runs/run_1" in response.headers["Location"]
    experiment = (
        web.EVALS_DIR / "experiments" / "experiment_abcdef123456.json"
    ).read_text()
    assert '"status": "finished"' in experiment
    assert '"run_id": "run_1"' in experiment


def test_runs_filter_by_prompt_rubric_pair(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    for run_id, prompt_id, rubric_id, created_at in [
        ("run_keep", "prompt_v1", "rubric_v1", "2026-07-16T16:25:02Z"),
        ("run_drop", "prompt_v2", "rubric_v1", "2026-07-16T17:07:00Z"),
        ("run_newer", "prompt_v1", "rubric_v1", "2026-07-16T17:07:00Z"),
    ]:
        atomic_write_json(web.EVALS_DIR / "runs" / run_id / "manifest.json", {
            "run_id": run_id,
            "case_id": "case",
            "agent_model": config.agent_model(),
            "judge_model": config.judge_model(),
            "prompt_id": prompt_id,
            "rubric_id": rubric_id,
            "created_at": created_at,
            "status": "judged",
        })
    body = client.get("/runs?prompt_id=prompt_v1&rubric_id=rubric_v1").get_data(as_text=True)
    assert "run_keep" in body
    assert "run_drop" not in body
    assert 'data-local-datetime="2026-07-16T16:25:02Z"' in body
    assert body.index("run_newer") < body.index("run_keep")


def test_review_requires_change_target_only_when_unacceptable(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    run_dir = web.EVALS_DIR / "runs" / "run_1"
    atomic_write_json(run_dir / "manifest.json", {
        "run_id": "run_1",
        "case_id": "case",
        "agent_model": config.agent_model(),
        "judge_model": config.judge_model(),
        "prompt_id": "prompt_v1",
        "rubric_id": "rubric_v1",
        "created_at": "t",
    })
    response = client.post("/runs/run_1/review", data={
        "verdict": "unacceptable",
        "failure_attribution": "",
    })
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "Choose what should change" in session["_flashes"][0][1]


def test_prompt_draft_builder_exposes_loading_and_lockable_controls(evals_dir, monkeypatch):
    reviews.create_review(
        "run_missing",
        "unacceptable",
        "Prompt missed a required behavior",
        "prompt_issue",
    )
    client = _client(evals_dir, monkeypatch)
    body = client.get("/").get_data(as_text=True)
    assert 'data-active-job="prompt_draft"' in body
    assert 'data-active-job-lock' in body
    assert "Generating new prompt…" in body
    assert 'name="job_id"' in body
    assert 'id="active-job-chip"' in body
    assert 'role="status" aria-live="polite" hidden' in body


def test_prompt_draft_job_persists_result_for_status_polling(evals_dir, monkeypatch):
    from harness import jobs, llm

    reviews.create_review(
        "run_missing",
        "unacceptable",
        "Prompt missed a required behavior",
        "prompt_issue",
    )
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "drafted prompt",
        "rationale": "fix it",
    })
    client = _client(evals_dir, monkeypatch)
    job_id = jobs.new_job_id()
    response = client.post("/versions/prompts/draft", data={
        "base_id": "prompt_v1",
        "review_ids": reviews.list_reviews()[0].review_id,
        "job_id": job_id,
    }, follow_redirects=False)
    assert response.status_code == 302
    assert f"/versions/prompts/draft/{job_id}" in response.headers["Location"]
    status = client.get(f"/jobs/{job_id}/status").get_json()
    assert status["status"] == "finished"
    assert status["kind"] == "prompt_draft"
    body = client.get(f"/versions/prompts/draft/{job_id}").get_data(as_text=True)
    assert "drafted prompt" in body


def test_markdown_preview_uses_server_renderer(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    response = client.post("/markdown/preview", json={
        "text": "# Heading\n\n- One\n- Two",
    })
    assert response.status_code == 200
    html = response.get_json()["html"]
    assert "<h1>Heading</h1>" in html
    assert "<li>One</li>" in html


def test_header_shows_active_models_and_versions_as_chips(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    body = client.get("/").get_data(as_text=True)
    assert "Active:" in body
    assert "👷" in body
    assert "⚖️" in body
    assert "claude-fable-5" in body
    assert "gpt-5.6-terra" in body
    assert 'href="/versions/prompts/prompt_v1"' in body
    assert 'href="/versions/rubrics/rubric_v1"' in body
    assert body.count("header-chip") >= 4


def test_prompt_and_rubric_version_editors_use_markdown_component(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    prompt_body = client.get("/versions/prompts/prompt_v1").get_data(as_text=True)
    assert 'data-markdown-editor' in prompt_body
    assert 'name="prompt_text"' in prompt_body
    assert "Save as next prompt version" in prompt_body

    rubric_body = client.get("/versions/rubrics/rubric_v1").get_data(as_text=True)
    assert 'data-markdown-editor' in rubric_body
    assert 'name="criteria_markdown"' in rubric_body
    assert "## " in rubric_body
    assert "Save as next rubric version" in rubric_body

    response = client.post("/versions/prompts/prompt_v1/save", data={
        "prompt_text": "# Updated prompt\n\nBe clearer.",
        "rationale": "tighten wording",
    })
    assert response.status_code == 302
    assert versions.load_prompt("prompt_v2").text.startswith("# Updated prompt")


def test_experiment_progress_message_multi_sample():
    from harness.web import _experiment_progress_message

    assert _experiment_progress_message(
        "checks",
        current_sample=2,
        completed_samples=1,
        samples=5,
    ) == "Sample 2 of 5 — Running deterministic checks…"


def test_chat_experiment_status_includes_progress(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    atomic_write_json(web.EVALS_DIR / "experiments" / "experiment_abcdef123456.json", {
        "experiment_id": "experiment_abcdef123456",
        "status": "running",
        "run_id": "run_1",
        "samples": 3,
        "phase": "judge",
        "current_sample": 2,
        "completed_samples": 1,
        "message": "Sample 2 of 3 — Judging answer…",
    })
    payload = client.get("/chat/experiments/experiment_abcdef123456/status").get_json()
    assert payload["status"] == "running"
    assert payload["phase"] == "judge"
    assert payload["current_sample"] == 2
    assert payload["message"] == "Sample 2 of 3 — Judging answer…"


def test_dashboard_pending_runs_have_no_delete_button(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    atomic_write_json(web.EVALS_DIR / "runs" / "run_pending" / "manifest.json", {
        "run_id": "run_pending",
        "case_id": "case",
        "agent_model": config.agent_model(),
        "judge_model": config.judge_model(),
        "prompt_id": "prompt_v1",
        "rubric_id": "rubric_v1",
        "created_at": "2026-07-16T17:07:00Z",
        "status": "judged",
    })
    body = client.get("/").get_data(as_text=True)
    assert "run_pending" in body
    assert "delete_run_route" not in body
    assert "subtle-danger" not in body.split("Pending runs")[1].split("Open reviews")[0]


def test_delete_run_route_rejects_dashboard_origin(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    atomic_write_json(web.EVALS_DIR / "runs" / "run_1" / "manifest.json", {
        "run_id": "run_1",
        "case_id": "case",
        "agent_model": config.agent_model(),
        "judge_model": config.judge_model(),
        "prompt_id": "prompt_v1",
        "rubric_id": "rubric_v1",
        "created_at": "t",
        "status": "judged",
    })
    response = client.post("/runs/run_1/delete")
    assert response.status_code == 302
    assert (web.EVALS_DIR / "runs" / "run_1").exists()
    with client.session_transaction() as session:
        assert "Delete runs from the Runs page" in session["_flashes"][0][1]


def test_chat_page_tracks_experiment_status_for_loading_ui(evals_dir, monkeypatch):
    client = _client(evals_dir, monkeypatch)
    body = client.get("/chat").get_data(as_text=True)
    assert 'name="experiment_id"' in body
    assert 'data-active-job="experiment"' in body
    assert "chat_experiment_status" in body or "/chat/experiments/" in body
    assert "__JOB_ID__" in body

    atomic_write_json(web.EVALS_DIR / "experiments" / "experiment_abcdef123456.json", {
        "experiment_id": "experiment_abcdef123456",
        "status": "finished",
        "run_id": "run_1",
        "samples": 1,
    })
    response = client.get("/chat/experiments/experiment_abcdef123456/status")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "finished"
    assert payload["run_id"] == "run_1"
    assert payload["result_url"].endswith("/runs/run_1")
