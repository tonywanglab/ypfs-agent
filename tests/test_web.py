from harness import config, dbio, feedback, runner, seed, tasks, versions, web
from harness.models import Case, RunManifest


def _client(pg, monkeypatch):
    seed.seed_all()
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    return web.create_app().test_client()


def _seed_run(run_id, prompt_id, created_at, case_id=None, status="complete", answer="q"):
    case_id = case_id or f"case_for_{run_id}"
    seed.insert_case(Case(case_id=case_id, prompt="q"))
    runner.save_manifest(
        RunManifest(
            run_id, case_id, config.agent_model(), prompt_id, created_at,
            status=status, sample_count=1,
        ),
        case_snapshot={"case_id": case_id, "prompt": "q", "tags": [], "notes": ""},
    )
    dbio.execute(
        "INSERT INTO run_samples (run_id, sample_index, answer, trace) VALUES (%s, %s, %s, %s)",
        (run_id, 1, answer, dbio.jsonb({"tool_calls": []})),
    )


def test_chat_exposes_only_the_prompt_variable(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    versions.save_prompt("prompt_v1", "second", "test")
    body = client.get("/chat").get_data(as_text=True)
    assert 'name="prompt_id"' in body
    assert 'name="rubric_id"' not in body
    assert 'name="model"' not in body
    assert config.agent_model() in body
    assert 'value="prompt_v2"' in body


def test_chat_submission_enqueues_task_with_selected_prompt_and_no_model_input(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    task_id = tasks.new_task_id()
    response = client.post("/chat/run", data={
        "query": "question",
        "prompt_id": "prompt_v1",
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
    assert "rubric_id" not in task["payload"]
    assert task["payload"]["samples"] == 3
    assert task["payload"]["case"]["prompt"] == "question"
    assert task["payload"]["agent_model"] == config.agent_model()


def test_runs_filter_by_prompt(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    versions.save_prompt("prompt_v1", "second", "test")  # allocates prompt_v2
    for run_id, prompt_id, created_at in [
        ("run_keep", "prompt_v1", "2026-07-16T16:25:02Z"),
        ("run_drop", "prompt_v2", "2026-07-16T17:07:00Z"),
        ("run_newer", "prompt_v1", "2026-07-16T17:07:00Z"),
    ]:
        _seed_run(run_id, prompt_id, created_at)
    body = client.get("/runs?prompt_id=prompt_v1").get_data(as_text=True)
    assert "run_keep" in body
    assert "run_drop" not in body
    assert 'data-local-datetime="2026-07-16T16:25:02Z"' in body
    assert body.index("run_newer") < body.index("run_keep")


def test_create_feedback_returns_201_and_appears_on_run_page(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t", answer="the agent's answer")

    response = client.post(
        "/runs/run_aaaaaaaaaaaa/feedback",
        json={"sample_index": 1, "selected_text": "the agent's answer", "comment": "too vague"},
    )
    assert response.status_code == 201
    body = response.get_json()["feedback"]
    assert body["feedback_id"].startswith("fb_")
    assert body["run_id"] == "run_aaaaaaaaaaaa"
    assert body["sample_index"] == 1

    page = client.get("/runs/run_aaaaaaaaaaaa").get_data(as_text=True)
    assert "the agent&#39;s answer" in page or "the agent's answer" in page
    assert "too vague" in page


def test_create_feedback_rejects_empty_comment(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    response = client.post(
        "/runs/run_aaaaaaaaaaaa/feedback",
        json={"sample_index": 1, "selected_text": "q", "comment": "   "},
    )
    assert response.status_code == 400


def test_create_feedback_rejects_unknown_sample_index(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    response = client.post(
        "/runs/run_aaaaaaaaaaaa/feedback",
        json={"sample_index": 99, "selected_text": "q", "comment": "note"},
    )
    assert response.status_code == 400


def test_create_feedback_rejects_unknown_run(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    response = client.post(
        "/runs/run_missing_000/feedback",
        json={"sample_index": 1, "selected_text": "q", "comment": "note"},
    )
    assert response.status_code == 404


def test_delete_feedback_route_removes_item_and_redirects(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    item = feedback.create_feedback("run_aaaaaaaaaaaa", 1, "q", "note")

    response = client.post(f"/feedback/{item.feedback_id}/delete")
    assert response.status_code == 302
    assert response.headers["Location"] == "/runs/run_aaaaaaaaaaaa#feedback"
    assert feedback.feedback_for_run("run_aaaaaaaaaaaa") == []


def test_delete_feedback_route_returns_json_when_requested(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    item = feedback.create_feedback("run_aaaaaaaaaaaa", 1, "q", "note")

    response = client.post(
        f"/feedback/{item.feedback_id}/delete",
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert body["feedback_id"] == item.feedback_id
    assert feedback.feedback_for_run("run_aaaaaaaaaaaa") == []


def test_draft_from_feedback_requires_at_least_one_item(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    response = client.post("/runs/run_aaaaaaaaaaaa/feedback/draft", data={"task_id": tasks.new_task_id()})
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "Add at least one feedback item" in session["_flashes"][0][1]


def test_draft_from_feedback_uses_latest_prompt_as_base(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    versions.save_prompt("prompt_v1", "current prompt text", "v2")
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t", answer="the agent's answer")
    feedback.create_feedback("run_aaaaaaaaaaaa", 1, "the agent's answer", "too vague")

    task_id = tasks.new_task_id()
    response = client.post("/runs/run_aaaaaaaaaaaa/feedback/draft", data={"task_id": task_id})
    assert response.status_code == 302
    task = tasks.load(task_id)
    assert task["payload"]["base_id"] == "prompt_v2"


def test_draft_from_feedback_runs_end_to_end_through_the_queue(pg, monkeypatch):
    from harness import llm, worker

    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t", answer="the agent's answer")
    feedback.create_feedback("run_aaaaaaaaaaaa", 1, "the agent's answer", "too vague")

    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "prompt_text": "drafted prompt",
        "rationale": "fix it",
    })
    task_id = tasks.new_task_id()
    response = client.post("/runs/run_aaaaaaaaaaaa/feedback/draft", data={"task_id": task_id}, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/runs/run_aaaaaaaaaaaa"

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
    assert "Current prompt vs generated draft" in body
    assert "prompt_v1" in body


def test_prompt_diff_endpoint_returns_html_diff(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    response = client.post("/versions/prompts/diff", json={
        "before": "alpha\nbeta",
        "after": "alpha\ngamma",
        "current_id": "prompt_v2",
    })
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "prompt_v2 → generated draft" in body
    assert "beta" in body
    assert "gamma" in body


def test_markdown_preview_uses_server_renderer(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    response = client.post("/markdown/preview", json={
        "text": "# Heading\n\n- One\n- Two",
    })
    assert response.status_code == 200
    html = response.get_json()["html"]
    assert "<h1>Heading</h1>" in html
    assert "<li>One</li>" in html


def test_header_shows_agent_model_and_prompt_version_chip(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    body = client.get("/").get_data(as_text=True)
    assert 'id="active-job-status"' in body
    assert "👷" in body
    assert "claude-fable-5" in body
    assert 'href="/versions/prompts/prompt_v1"' in body


def test_prompt_version_editor_uses_markdown_component(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    prompt_body = client.get("/versions/prompts/prompt_v1").get_data(as_text=True)
    assert 'data-markdown-editor' in prompt_body
    assert 'name="prompt_text"' in prompt_body
    assert "Save" in prompt_body

    response = client.post("/versions/prompts/prompt_v1/save", data={
        "prompt_text": "# Updated prompt\n\nBe clearer.",
        "rationale": "tighten wording",
    })
    assert response.status_code == 302
    assert versions.load_prompt("prompt_v2").text.startswith("# Updated prompt")


def test_task_status_endpoint_includes_progress_and_result_url(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    task_id = tasks.new_task_id()
    tasks.enqueue(
        tasks.KIND_EXPERIMENT,
        payload={
            "case": {"case_id": "c", "prompt": "q", "tags": [], "notes": ""},
            "prompt_id": "prompt_v1",
            "samples": 1,
        },
        task_id=task_id,
    )
    tasks.set_run(task_id, "run_aaaaaaaaaaaa")
    tasks.set_progress(
        task_id,
        phase="agent",
        current_sample=1,
        completed_samples=0,
        message="Running agent…",
    )
    payload = client.get(f"/tasks/{task_id}/status").get_json()
    assert payload["status"] == "queued"
    assert payload["progress"]["phase"] == "agent"
    assert payload["progress"]["current_sample"] == 1
    assert payload["progress"]["message"] == "Running agent…"
    assert payload["run_id"] == "run_aaaaaaaaaaaa"
    assert payload["result_url"] == "/runs/run_aaaaaaaaaaaa"


def test_dashboard_lists_recent_runs(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_recent", "prompt_v1", "2026-07-16T17:07:00Z")
    body = client.get("/").get_data(as_text=True)
    assert "run_recent" in body


def test_dashboard_recent_runs_hide_pending_and_experiment_prefix(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_pending", "prompt_v1", "2026-07-16T17:07:00Z", status="pending")
    _seed_run(
        "run_done",
        "prompt_v1",
        "2026-07-16T18:07:00Z",
        answer="What is liquidity support?",
    )
    dbio.execute(
        "UPDATE runs SET case_snapshot = %s WHERE run_id = %s",
        (
            dbio.jsonb({
                "case_id": "case_for_run_done",
                "prompt": "What is liquidity support?",
                "tags": [],
                "notes": "",
            }),
            "run_done",
        ),
    )
    body = client.get("/").get_data(as_text=True)
    assert "What is liquidity support?" in body
    assert "run_pending" not in body
    assert "experiment:" not in body


def test_delete_run_route_rejects_dashboard_origin(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    response = client.post("/runs/run_aaaaaaaaaaaa/delete")
    assert response.status_code == 302
    assert runner.load_manifest("run_aaaaaaaaaaaa").run_id == "run_aaaaaaaaaaaa"
    with client.session_transaction() as session:
        assert "Delete runs from the Runs page" in session["_flashes"][0][1]


def test_delete_run_route_rejects_invalid_run_id(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    response = client.post("/runs/not-a-real-id/delete", data={"next": "runs"})
    assert response.status_code == 404


def test_delete_run_route_cascades_feedback(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    _seed_run("run_aaaaaaaaaaaa", "prompt_v1", "t")
    feedback.create_feedback("run_aaaaaaaaaaaa", 1, "q", "note")

    response = client.post("/runs/run_aaaaaaaaaaaa/delete", data={"next": "runs"})
    assert response.status_code == 302
    assert feedback.feedback_for_run("run_aaaaaaaaaaaa") == []


def test_chat_page_tracks_experiments_without_locking_the_form(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    body = client.get("/chat").get_data(as_text=True)
    assert 'name="task_id"' in body
    assert 'data-active-job="experiment"' in body
    assert "data-active-job-track-only" in body
    assert "data-active-job-lock" not in body


def test_chat_page_lists_queued_runs_and_allows_queuing_another(pg, monkeypatch):
    client = _client(pg, monkeypatch)
    first_task = tasks.new_task_id()
    response = client.post("/chat/run", data={
        "query": "first question",
        "prompt_id": "prompt_v1",
        "samples": "1",
        "task_id": first_task,
    })
    assert response.status_code == 302

    second_task = tasks.new_task_id()
    response = client.post("/chat/run", data={
        "query": "second question",
        "prompt_id": "prompt_v1",
        "samples": "1",
        "task_id": second_task,
    })
    assert response.status_code == 302

    body = client.get("/chat").get_data(as_text=True)
    assert first_task in body
    assert second_task in body
    assert tasks.load(first_task)["status"] == "queued"
    assert tasks.load(second_task)["status"] == "queued"
