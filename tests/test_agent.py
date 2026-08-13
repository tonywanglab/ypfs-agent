from __future__ import annotations

import importlib


def test_run_reloads_default_system_prompt_each_call(tmp_path, monkeypatch):
    agent = importlib.import_module("agent.agent")
    prompt_path = tmp_path / "system_prompt.md"
    prompt_path.write_text("first prompt")
    monkeypatch.setattr(agent, "SYSTEM_PROMPT_PATH", prompt_path)
    captured = []

    def fake_call(messages, model, tools):
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

    def fake_call(messages, model, tools):
        captured.append(list(messages))
        return {"role": "assistant", "content": "done"}

    monkeypatch.setattr(agent, "_call", fake_call)
    agent.run("question", model="model-x", system_prompt=None)

    assert captured[0] == [{"role": "user", "content": "question"}]


def test_run_defaults_to_the_module_tool_registry(monkeypatch):
    """Regression guard: callers that pass no tools/dispatch_fn must get
    exactly the pre-existing behavior — the full registry and its dispatch."""
    agent = importlib.import_module("agent.agent")
    from agent import tools as tools_mod

    seen = {}

    def fake_call(messages, model, tools):
        seen["tools"] = tools
        return {"role": "assistant", "content": "done"}

    monkeypatch.setattr(agent, "_call", fake_call)
    agent.run("question", model="model-x", system_prompt=None)

    assert seen["tools"] is tools_mod.TOOLS


def test_run_sends_caller_supplied_tools_and_dispatch(monkeypatch):
    agent = importlib.import_module("agent.agent")
    extra = {"type": "function", "function": {"name": "extra_tool", "parameters": {}}}
    sent_tools = []
    dispatched = []

    def fake_call(messages, model, tools):
        sent_tools.append(tools)
        # Call the extra tool once, then finish on the second turn.
        if len(sent_tools) == 1:
            return {
                "role": "assistant",
                "tool_calls": [{
                    "id": "call_1",
                    "function": {"name": "extra_tool", "arguments": '{"x": 1}'},
                }],
            }
        return {"role": "assistant", "content": "done"}

    def fake_dispatch(name, args, context):
        dispatched.append((name, args, context))
        return {"ok": True}

    monkeypatch.setattr(agent, "_call", fake_call)
    answer, messages = agent.run(
        "question", model="model-x", system_prompt=None,
        tools=[extra], dispatch_fn=fake_dispatch,
    )

    assert answer == "done"
    assert sent_tools[0] == [extra]
    assert [name for name, _, _ in dispatched] == ["extra_tool"]
    assert dispatched[0][1] == {"x": 1}
    assert any(m.get("role") == "tool" for m in messages)
