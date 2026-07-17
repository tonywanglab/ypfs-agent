from harness import config, reviews, runner, seed, tasks, versions, web
from harness.models import Case, RunManifest


def _client(pg, monkeypatch):
    seed.seed_all()
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    return web.create_app().test_client()


def _seed_run(run_id, prompt_id, rubric_id, created_at, case_id=None, status="judged"):
    case_id = case_id or f"case_for_{run_id}"
    seed.insert_case(Case(case_id=case_id, prompt="q"))
    runner.save_manifest(
        RunManifest(
            run_id, case_id, config.agent_model(), config.judge_model(),
            prompt_id, rubric_id, created_at, status=status, sample_count=1,
        ),
        case_snapshot={"case_id": case_id, "prompt": "q", "tags": [], "notes": ""},
    )


def test_chat_exposes_only_prompt_and_rubric_variables(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    versions.save_prompt("prompt_v1", "second", "test", [])
    body = client.get("/chat").get_data(as_text=True)
    assert 'name="prompt_id"' in body
    assert 'name="rubric_id"' in body
    assert 'name="model"' not in body
    assert config.agent_model() in body
    assert config.judge_model() in body
    assert 'value="prompt_v2"' in body


def test_chat_submission_enqueues_task_with_selected_pair_and_no_model_input(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    task_id = tasks.new_task_id()
    response = client.post("/chat/run", data={
        "query": "question",
        "prompt_id": "prompt_v1",
        "rubric_id": "rubric_v1",
        "samples": "3",
        "task_id": task_id,
        "model": "malicious/override",
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/chat"
    task = tasks.load(task_id)
    assert task["kind"] == "experiment"
    assert task["status"] == "queued"
    assert task["payload"]["prompt_id"] == "prompt_v1"
    assert task["payload"]["rubric_id"] == "rubric_v1"
    assert task["payload"]["samples"] == 3
    assert task["payload"]["case"]["prompt"] == "question"
    assert task["payload"]["agent_model"] == config.agent_model()


def test_runs_filter_by_prompt_rubric_pair(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    versions.save_prompt("prompt_v1", "second", "test", [])  # allocates prompt_v2
    for run_id, prompt_id, rubric_id, created_at in [
        ("run_keep", "prompt_v1", "rubric_v1", "2026-07-16T16:25:02Z"),
        ("run_drop", "prompt_v2", "rubric_v1", "2026-07-16T17:07:00Z"),
        ("run_newer", "prompt_v1", "rubric_v1", "2026-07-16T17:07:00Z"),
    ]:
        _seed_run(run_id, prompt_id, rubric_id, created_at)
    body = client.get("/runs?prompt_id=prompt_v1&rubric_id=rubric_v1").get_data(as_text=True)
    assert "run_keep" in body
    assert "run_drop" not in body
    assert 'data-local-datetime="2026-07-16T16:25:02Z"' in body
    assert body.index("run_newer") < body.index("run_keep")


def test_review_requires_change_target_only_when_unacceptable(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_1", "prompt_v1", "rubric_v1", "t")
    response = client.post("/runs/run_1/review", data={
        "verdict": "unacceptable",
        "failure_attribution": "",
    })
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "Choose what should change" in session["_flashes"][0][1]


def test_prompt_draft_builder_exposes_loading_and_lockable_controls(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_1", "prompt_v1", "rubric_v1", "t")
    reviews.create_review(
        "run_1",
        "unacceptable",
        "Prompt missed a required behavior",
        "prompt_issue",
    )
    body = client.get("/").get_data(as_text=True)
    assert 'data-active-job="prompt_draft"' in body
    assert 'data-active-job-lock' in body
    assert "Generating new prompt…" in body
    assert 'name="task_id"' in body
    assert 'id="active-job-chip"' in body
    assert 'role="status" aria-live="polite" hidden' in body


def test_prompt_draft_task_runs_end_to_end_through_the_queue(pg, monkeypatch):
    from harness import llm, worker

    client = _client(pg, monkeypatch)
    _seed_run("run_1", "prompt_v1", "rubric_v1", "t")
    review = reviews.create_review(
        "run_1",
        "unacceptable",
        "Prompt missed a required behavior",
        "prompt_issue",
    )
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "drafted prompt",
        "rationale": "fix it",
    })
    task_id = tasks.new_task_id()
    response = client.post("/versions/prompts/draft", data={
        "base_id": "prompt_v1",
        "review_ids": review.review_id,
        "task_id": task_id,
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    status = client.get(f"/tasks/{task_id}/status").get_json()
    assert status["status"] == "queued"
    assert status["kind"] == "prompt_draft"

    claimed = tasks.claim("test-worker")
    assert claimed["task_id"] == task_id
    worker.execute_task(claimed)

    status = client.get(f"/tasks/{task_id}/status").get_json()
    assert status["status"] == "finished"
    body = client.get(f"/versions/prompts/draft/{task_id}").get_data(as_text=True)
    assert "drafted prompt" in body


def test_markdown_preview_uses_server_renderer(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    response = client.post("/markdown/preview", json={
        "text": "# Heading\n\n- One\n- Two",
    })
    assert response.status_code == 200
    html = response.get_json()["html"]
    assert "<h1>Heading</h1>" in html
    assert "<li>One</li>" in html


def test_header_shows_active_models_and_versions_as_chips(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    body = client.get("/").get_data(as_text=True)
    assert "Active:" in body
    assert "👷" in body
    assert "⚖️" in body
    assert "claude-fable-5" in body
    assert "gpt-5.6-terra" in body
    assert 'href="/versions/prompts/prompt_v1"' in body
    assert 'href="/versions/rubrics/rubric_v1"' in body
    assert body.count("header-chip") >= 4


def test_prompt_and_rubric_version_editors_use_markdown_component(pg, monkeypatch):
    client = _client(pg, monkeypatch)
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


def test_task_status_endpoint_includes_progress_and_result_url(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_1", "prompt_v1", "rubric_v1", "t")
    task_id = tasks.new_task_id()
    tasks.enqueue(
        tasks.KIND_EXPERIMENT,
        payload={
            "case": {"case_id": "c", "prompt": "q", "tags": [], "notes": ""},
            "prompt_id": "prompt_v1",
            "rubric_id": "rubric_v1",
            "samples": 1,
        },
        task_id=task_id,
    )
    tasks.set_run(task_id, "run_1")
    tasks.set_progress(
        task_id,
        phase="judge",
        current_sample=2,
        completed_samples=1,
        message="Sample 2 of 3 — Judging answer…",
    )
    payload = client.get(f"/tasks/{task_id}/status").get_json()
    assert payload["status"] == "queued"
    assert payload["progress"]["phase"] == "judge"
    assert payload["progress"]["current_sample"] == 2
    assert payload["progress"]["message"] == "Sample 2 of 3 — Judging answer…"
    assert payload["run_id"] == "run_1"
    assert payload["result_url"] == "/runs/run_1"


def test_dashboard_pending_runs_have_no_delete_button(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_pending", "prompt_v1", "rubric_v1", "2026-07-16T17:07:00Z")
    body = client.get("/").get_data(as_text=True)
    assert "run_pending" in body
    assert "delete_run_route" not in body
    assert "subtle-danger" not in body.split("Pending runs")[1].split("Open reviews")[0]


def test_delete_run_route_rejects_dashboard_origin(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_1", "prompt_v1", "rubric_v1", "t")
    response = client.post("/runs/run_1/delete")
    assert response.status_code == 302
    assert runner.load_manifest("run_1").run_id == "run_1"
    with client.session_transaction() as session:
        assert "Delete runs from the Runs page" in session["_flashes"][0][1]


def test_delete_run_route_rejects_invalid_run_id(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    response = client.post("/runs/not-a-real-id/delete", data={"next": "runs"})
    assert response.status_code == 404


def test_chat_page_tracks_task_status_for_loading_ui(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    body = client.get("/chat").get_data(as_text=True)
    assert 'name="task_id"' in body
    assert 'data-active-job="experiment"' in body
    assert "task_status" in body or "/tasks/" in body
    assert "__JOB_ID__" in body
