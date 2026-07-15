from __future__ import annotations

import importlib


def test_run_reloads_default_system_prompt_each_call(tmp_path, monkeypatch):
    agent = importlib.import_module("agent.agent")
    prompt_path = tmp_path / "system_prompt.md"
    prompt_path.write_text("first prompt")
    monkeypatch.setattr(agent, "SYSTEM_PROMPT_PATH", prompt_path)
    captured = []

    def fake_call(messages, model):
        captured.append(list(messages))
        return {"role": "assistant", "content": "done"}

    monkeypatch.setattr(agent, "_call", fake_call)
    agent.run("question one", model="model-x")
    prompt_path.write_text("second prompt")
    agent.run("question two", model="model-x")

    assert captured[0][0] == {"role": "system", "content": "first prompt"}
    assert captured[1][0] == {"role": "system", "content": "second prompt"}


def test_run_can_explicitly_omit_system_prompt(monkeypatch):
    agent = importlib.import_module("agent.agent")
    captured = []

    def fake_call(messages, model):
        captured.append(list(messages))
        return {"role": "assistant", "content": "done"}

    monkeypatch.setattr(agent, "_call", fake_call)
    agent.run("question", model="model-x", system_prompt=None)

    assert captured[0] == [{"role": "user", "content": "question"}]
