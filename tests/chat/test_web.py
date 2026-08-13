"""Route-level tests for the chat blueprint: the role gate and the transcript."""

from __future__ import annotations

import pytest

from harness import web
from harness.chat import conversations


def _client(monkeypatch, password="s3cret"):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    if password is None:
        monkeypatch.delenv("HARNESS_ADMIN_PASSWORD", raising=False)
    else:
        monkeypatch.setenv("HARNESS_ADMIN_PASSWORD", password)
    return web.create_app().test_client()


def _login(client, password="s3cret"):
    response = client.post("/login", data={"password": password})
    assert response.status_code in (302, 403), response.status_code
    return response


# ---- Auth ----------------------------------------------------------------

def test_login_refuses_when_no_password_is_configured(seeded, monkeypatch):
    client = _client(monkeypatch, password=None)
    body = client.get("/login").get_data(as_text=True)
    assert "not configured" in body
    # An empty submission must not be accepted just because the env is unset.
    assert client.post("/login", data={"password": ""}).status_code == 403
    assert client.get("/").status_code in (302, 403)


def test_wrong_password_is_refused(seeded, monkeypatch):
    client = _client(monkeypatch)
    assert client.post("/login", data={"password": "nope"}).status_code == 403
    assert client.get("/golden").status_code in (302, 403)


def test_correct_password_unlocks_the_eval_console(seeded, monkeypatch):
    client = _client(monkeypatch)
    assert _login(client).status_code == 302
    assert client.get("/").status_code == 200
    assert client.get("/golden").status_code == 200


def test_user_role_is_denied_the_eval_console_and_golden(seeded, monkeypatch):
    client = _client(monkeypatch)
    # GET from a browser redirects to login; a POST is refused outright.
    assert client.get("/runs").status_code == 302
    assert client.get("/golden").status_code == 302
    assert client.post("/golden/mark", data={}).status_code == 403
    assert client.get("/golden", headers={"X-Requested-With": "XMLHttpRequest"}).status_code == 403


def test_logout_drops_back_to_user(seeded, monkeypatch):
    client = _client(monkeypatch)
    _login(client)
    assert client.get("/golden").status_code == 200
    client.post("/logout")
    assert client.get("/golden").status_code == 302


def test_clearing_the_password_revokes_an_existing_admin_session(seeded, monkeypatch):
    """A session should not outlive the configuration that authorized it."""
    client = _client(monkeypatch)
    _login(client)
    assert client.get("/golden").status_code == 200
    monkeypatch.delenv("HARNESS_ADMIN_PASSWORD", raising=False)
    assert client.get("/golden").status_code == 302


# ---- Conversations -------------------------------------------------------

def test_user_can_start_and_view_a_conversation(seeded, monkeypatch):
    client = _client(monkeypatch)
    created = client.post("/c")
    assert created.status_code == 302
    location = created.headers["Location"]
    assert client.get(location).status_code == 200
    assert client.get("/c").status_code == 200


def test_user_cannot_open_an_admin_conversation_by_id(seeded, monkeypatch):
    client = _client(monkeypatch)
    conv = conversations.create("admin")
    assert client.get(f"/c/{conv.conversation_id}").status_code == 404


def test_malformed_conversation_id_is_404(seeded, monkeypatch):
    client = _client(monkeypatch)
    assert client.get("/c/not-an-id").status_code == 404


def test_posting_a_message_creates_a_turn_and_queues_a_task(seeded, monkeypatch):
    from harness import tasks

    client = _client(monkeypatch)
    conv = conversations.create("user")
    response = client.post(f"/c/{conv.conversation_id}/messages",
                           data={"query": "what happened in 2008?"})
    assert response.status_code == 302

    turns = conversations.turns_for(conv.conversation_id)
    assert [t.query for t in turns] == ["what happened in 2008?"]

    queued = [t for t in tasks.list_active() if t["kind"] == "chat_turn"]
    assert len(queued) == 1
    assert queued[0]["payload"]["turn_id"] == turns[0].turn_id
    # A user conversation must not get the prompt-editing tool.
    assert queued[0]["payload"]["is_admin"] is False


def test_admin_conversation_queues_an_admin_run(seeded, monkeypatch):
    from harness import tasks

    client = _client(monkeypatch)
    _login(client)
    created = client.post("/c")
    conversation_id = created.headers["Location"].rsplit("/", 1)[-1]
    client.post(f"/c/{conversation_id}/messages", data={"query": "hello"})

    queued = [t for t in tasks.list_active() if t["kind"] == "chat_turn"]
    assert queued[0]["payload"]["is_admin"] is True


def test_quoted_span_is_stored_on_the_turn(seeded, monkeypatch, make_chat_run):
    client = _client(monkeypatch)
    conv = conversations.create("user")
    first = conversations.add_turn(conv.conversation_id, "first")
    run_id = make_chat_run(first.turn_id, answer="Bagehot argued for lending freely.")

    client.post(f"/c/{conv.conversation_id}/messages", data={
        "query": "that over-cites a primary source",
        "quoted_text": "Bagehot argued for lending freely.",
        "quoted_run_id": run_id,
    })

    second = conversations.turns_for(conv.conversation_id)[1]
    assert second.query == "that over-cites a primary source"
    assert second.quoted_text == "Bagehot argued for lending freely."
    assert second.quoted_run_id == run_id


def test_empty_message_is_rejected_without_creating_a_turn(seeded, monkeypatch):
    client = _client(monkeypatch)
    conv = conversations.create("user")
    client.post(f"/c/{conv.conversation_id}/messages", data={"query": "   "})
    assert conversations.turns_for(conv.conversation_id) == []


def test_transcript_shows_answer_trace_and_previous_responses(seeded, monkeypatch,
                                                              make_chat_run):
    client = _client(monkeypatch)
    _login(client)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    make_chat_run(turn.turn_id, answer="first attempt", trace={
        "messages": [
            {"role": "assistant", "tool_calls": [
                {"id": "c1", "function": {"name": "search_corpus",
                                           "arguments": '{"query": "runs"}'}}]},
            {"role": "tool", "name": "search_corpus", "tool_call_id": "c1",
             "content": '{"results": []}'},
            {"role": "assistant", "content": "first attempt"},
        ],
    })
    make_chat_run(turn.turn_id, answer="second attempt")

    body = client.get(f"/c/{conv.conversation_id}").get_data(as_text=True)
    assert "second attempt" in body          # active response inline
    assert "Previous response" in body       # the old one folded away
    assert "first attempt" in body           # still present, in the accordion
    assert "Tool trace" in body
    assert "search_corpus" in body
    # The query is rendered once even though there are two responses.
    assert body.count("the question") == 1


def test_user_transcript_hides_admin_controls(seeded, monkeypatch, make_chat_run):
    client = _client(monkeypatch)
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "a question")
    make_chat_run(turn.turn_id, answer="an answer", trace={
        "messages": [
            {"role": "assistant", "tool_calls": [
                {"id": "c1", "function": {"name": "search_corpus",
                                           "arguments": '{"query": "runs"}'}}]},
            {"role": "tool", "name": "search_corpus", "tool_call_id": "c1",
             "content": '{"results": []}'},
            {"role": "assistant", "content": "an answer"},
        ],
    })

    body = client.get(f"/c/{conv.conversation_id}").get_data(as_text=True)
    assert "an answer" in body
    # The trace is for everyone — it's how you see what the agent actually read.
    assert "Tool trace" in body
    assert "search_corpus" in body
    # Curation and prompt controls are not.
    assert "Mark golden" not in body
    assert "Re-answer" not in body
    assert "prompt_v1" not in body


def test_status_endpoint_reports_progress_without_leaking_the_prompt(seeded, monkeypatch):
    client = _client(monkeypatch)
    conv = conversations.create("user")
    client.post(f"/c/{conv.conversation_id}/messages", data={"query": "hello"})

    payload = client.get(f"/c/{conv.conversation_id}/status").get_json()
    assert payload["turns"] == 1
    assert payload["answered"] == 0
    assert payload["pending"] == 1
    assert payload["failed"] == 0
    assert "prompt_v1" not in str(payload)


def test_status_reports_a_failed_run_so_the_client_stops_polling(seeded, monkeypatch,
                                                                make_chat_run):
    """The client distinguishes "failed" from "not queued yet" via this field.

    Without it, a turn whose run failed leaves pending=0 and an unanswered turn
    forever, and a client that reloads on that condition reloads on every load —
    an endless refresh storm.
    """
    from harness import tasks

    client = _client(monkeypatch)
    conv = conversations.create("user")
    client.post(f"/c/{conv.conversation_id}/messages", data={"query": "hello"})
    queued = [t for t in tasks.list_active() if t["kind"] == "chat_turn"][0]
    tasks.claim("w")
    tasks.fail(queued["task_id"], "worker exploded")

    payload = client.get(f"/c/{conv.conversation_id}/status").get_json()
    assert payload["pending"] == 0
    assert payload["answered"] == 0
    assert payload["turns"] == 1
    assert payload["failed"] == 1


def test_answer_counts_matches_per_turn_lookups(seeded, make_chat_run):
    """answer_counts is the one-query version of counting active_run() per turn;
    they must not drift apart."""
    conv = conversations.create("user")
    answered_turn = conversations.add_turn(conv.conversation_id, "answered")
    make_chat_run(answered_turn.turn_id, answer="yes")
    conversations.add_turn(conv.conversation_id, "unanswered")

    turns = conversations.turns_for(conv.conversation_id)
    by_hand = sum(1 for t in turns if conversations.active_run(t.turn_id) is not None)
    counts = conversations.answer_counts(conv.conversation_id)
    assert counts == {"turns": len(turns), "answered": by_hand}
    assert counts == {"turns": 2, "answered": 1}


def test_regenerate_is_admin_only(seeded, monkeypatch, make_chat_run):
    client = _client(monkeypatch)
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "q")
    make_chat_run(turn.turn_id)
    url = f"/c/{conv.conversation_id}/turns/{turn.turn_id}/regenerate"
    assert client.post(url).status_code == 403


def test_delete_conversation_removes_it(seeded, monkeypatch):
    client = _client(monkeypatch)
    conv = conversations.create("user")
    assert client.post(f"/c/{conv.conversation_id}/delete").status_code == 302
    with pytest.raises(FileNotFoundError):
        conversations.load(conv.conversation_id)
