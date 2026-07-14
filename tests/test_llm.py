from __future__ import annotations

import json

import pytest
import requests

from harness import llm


def test_parse_json_object_direct():
    assert llm.parse_json_object('{"a": 1}') == {"a": 1}


def test_parse_json_object_strips_surrounding_prose_and_fences():
    text = 'Sure, here is the result:\n```json\n{"a": 1, "b": [1,2]}\n```\nHope that helps.'
    assert llm.parse_json_object(text) == {"a": 1, "b": [1, 2]}


def test_parse_json_object_raises_on_garbage():
    with pytest.raises(llm.LLMError):
        llm.parse_json_object("not json at all")


def test_chat_json_parses_first_valid_response(monkeypatch):
    calls = []

    def fake_chat(messages, model, tools=None, json_mode=False):
        calls.append(messages)
        return {"role": "assistant", "content": '{"ok": true}'}

    monkeypatch.setattr(llm, "chat", fake_chat)
    result = llm.chat_json("sys", "user", "model-x")
    assert result == {"ok": True}
    assert len(calls) == 1


def test_chat_json_retries_once_on_malformed_json(monkeypatch):
    responses = iter([
        {"role": "assistant", "content": "not json"},
        {"role": "assistant", "content": '{"ok": true}'},
    ])

    def fake_chat(messages, model, tools=None, json_mode=False):
        return next(responses)

    monkeypatch.setattr(llm, "chat", fake_chat)
    result = llm.chat_json("sys", "user", "model-x", max_attempts=2)
    assert result == {"ok": True}


def test_chat_json_raises_after_exhausting_attempts(monkeypatch):
    def fake_chat(messages, model, tools=None, json_mode=False):
        return {"role": "assistant", "content": "still not json"}

    monkeypatch.setattr(llm, "chat", fake_chat)
    with pytest.raises(llm.LLMError):
        llm.chat_json("sys", "user", "model-x", max_attempts=2)


def test_run_tool_loop_returns_immediately_without_tool_calls(monkeypatch):
    def fake_chat(messages, model, tools=None, json_mode=False):
        return {"role": "assistant", "content": "final answer"}

    monkeypatch.setattr(llm, "chat", fake_chat)
    content, messages = llm.run_tool_loop("sys", "hi", "model-x", tools=[], dispatch_fn=None)
    assert content == "final answer"
    assert messages[0] == {"role": "user", "content": "hi"}


def test_run_tool_loop_dispatches_calls_then_returns_final_answer(monkeypatch):
    step = {"n": 0}

    def fake_chat(messages, model, tools=None, json_mode=False):
        step["n"] += 1
        if step["n"] == 1:
            return {
                "role": "assistant", "content": None,
                "tool_calls": [{"id": "c1", "function": {"name": "search_corpus",
                                                            "arguments": json.dumps({"query": "x"})}}],
            }
        return {"role": "assistant", "content": "done searching"}

    def fake_dispatch(name, args):
        assert name == "search_corpus"
        return {"results": [{"doc_id": "vol1_iss1_1"}], "total_found": 1}

    monkeypatch.setattr(llm, "chat", fake_chat)
    content, messages = llm.run_tool_loop("sys", "hi", "model-x", tools=[{"schema": True}],
                                           dispatch_fn=fake_dispatch)
    assert content == "done searching"
    tool_msgs = [m for m in messages if m["role"] == "tool"]
    assert len(tool_msgs) == 1
    assert json.loads(tool_msgs[0]["content"])["results"][0]["doc_id"] == "vol1_iss1_1"


def test_run_tool_loop_hits_max_steps(monkeypatch):
    def fake_chat(messages, model, tools=None, json_mode=False):
        return {
            "role": "assistant", "content": None,
            "tool_calls": [{"id": "c", "function": {"name": "search_corpus", "arguments": "{}"}}],
        }

    def fake_dispatch(name, args):
        return {"results": [], "total_found": 0}

    monkeypatch.setattr(llm, "chat", fake_chat)
    content, _ = llm.run_tool_loop("sys", "hi", "model-x", tools=[], dispatch_fn=fake_dispatch,
                                    max_steps=2)
    assert content == "[stopped: hit MAX_STEPS]"


def test_chat_retries_on_429_then_succeeds(monkeypatch):
    """chat() retries transient errors — mirrors agent.agent._call's policy."""
    attempts = {"n": 0}

    class FakeResponse:
        def __init__(self, status_code):
            self.status_code = status_code
            self.headers = {}

        def raise_for_status(self):
            if self.status_code >= 400:
                err = requests.HTTPError(response=self)
                raise err

        def json(self):
            return {"choices": [{"message": {"role": "assistant", "content": "ok"}}]}

    def fake_post(*args, **kwargs):
        attempts["n"] += 1
        return FakeResponse(429 if attempts["n"] == 1 else 200)

    monkeypatch.setattr(llm.requests, "post", fake_post)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    msg = llm.chat([{"role": "user", "content": "hi"}], "model-x")
    assert msg["content"] == "ok"
    assert attempts["n"] == 2
