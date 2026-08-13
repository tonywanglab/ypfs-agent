"""The chat task executor, with the agent mocked.

This is where the pieces meet: history replay, the admin tool seam, the
chat_run_links row, and the revision/stale bookkeeping after a regeneration.
"""

from __future__ import annotations

from harness import tasks, versions, worker
from harness.chat import admin_tools, conversations, runs


def _fake_agent(monkeypatch, answer="an answer", record=None, on_call=None):
    """Replace agent.run at the seam harness.runner imports it from."""
    def fake_agent_run(user_msg, history=None, model=None, system_prompt=None,
                       context=None, tools=None, dispatch_fn=None):
        if record is not None:
            record.append({
                "user_msg": user_msg,
                "history": list(history or []),
                "system_prompt": system_prompt,
                "tools": tools,
                "dispatch_fn": dispatch_fn,
                "context": context,
            })
        if on_call is not None:
            on_call(context, dispatch_fn)
        return answer, [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": answer},
        ]

    monkeypatch.setattr("harness.runner.agent_run", fake_agent_run)


def _drain():
    """Claim and execute every queued task, as a worker would."""
    executed = []
    while True:
        task = tasks.claim("test-worker")
        if task is None:
            return executed
        worker.execute_task(task)
        executed.append(tasks.load(task["task_id"]))


def test_a_chat_turn_runs_and_links_its_run(seeded, monkeypatch):
    _fake_agent(monkeypatch, answer="the answer")
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=False)

    finished = _drain()
    assert [t["status"] for t in finished] == ["finished"]

    active = conversations.active_run(turn.turn_id)
    assert active["answer"] == "the answer"
    assert active["revision_index"] == 1
    assert active["prompt_id"] == "prompt_v1"


def test_the_first_turn_names_the_conversation(seeded, monkeypatch):
    _fake_agent(monkeypatch)
    conv = conversations.create("user")
    assert conv.title == ""
    turn = conversations.add_turn(conv.conversation_id, "what caused the 2008 crisis?")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=False)
    _drain()
    assert conversations.load(conv.conversation_id).title == "what caused the 2008 crisis?"


def test_a_quoted_turn_sends_the_quote_to_the_model(seeded, monkeypatch):
    record = []
    _fake_agent(monkeypatch, record=record)
    conv = conversations.create("user")
    turn = conversations.add_turn(
        conv.conversation_id, "why?", quoted_text="Deposit flight did.",
    )
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=False)
    _drain()

    assert "> Deposit flight did." in record[0]["user_msg"]
    assert record[0]["user_msg"].endswith("why?")
    # The turn row still stores only what was typed.
    assert conversations.load_turn(turn.turn_id).query == "why?"


def test_the_second_turn_receives_the_first_as_history(seeded, monkeypatch):
    record = []
    _fake_agent(monkeypatch, answer="first answer", record=record)
    conv = conversations.create("user")
    first = conversations.add_turn(conv.conversation_id, "first question")
    runs.enqueue_turn(conv.conversation_id, first.turn_id, "prompt_v1", is_admin=False)
    _drain()

    assert record[0]["history"] == []

    second = conversations.add_turn(conv.conversation_id, "second question")
    runs.enqueue_turn(conv.conversation_id, second.turn_id, "prompt_v1", is_admin=False)
    _drain()

    history = record[1]["history"]
    assert [m["content"] for m in history] == ["first question", "first answer"]


def test_user_runs_get_no_tools_override_and_admin_runs_do(seeded, monkeypatch):
    record = []
    _fake_agent(monkeypatch, record=record)

    user_conv = conversations.create("user")
    user_turn = conversations.add_turn(user_conv.conversation_id, "q")
    runs.enqueue_turn(user_conv.conversation_id, user_turn.turn_id, "prompt_v1",
                      is_admin=False)
    _drain()

    admin_conv = conversations.create("admin")
    admin_turn = conversations.add_turn(admin_conv.conversation_id, "q")
    runs.enqueue_turn(admin_conv.conversation_id, admin_turn.turn_id, "prompt_v1",
                      is_admin=True)
    _drain()

    # User run: agent.run's defaults, i.e. the plain registry.
    assert record[0]["tools"] is None
    assert record[0]["dispatch_fn"] is None
    assert record[0]["context"].is_admin is False

    # Admin run: the extra tool, and a dispatch that knows it.
    admin_tool_names = [t["function"]["name"] for t in record[1]["tools"]]
    assert admin_tools.TOOL_NAME in admin_tool_names
    assert record[1]["dispatch_fn"] is admin_tools.dispatch
    assert record[1]["context"].is_admin is True


def test_the_context_carries_a_run_id_before_the_agent_is_called(seeded, monkeypatch):
    """The prompt-revision tool attaches its proposal to a run, so the run must
    already exist by the time the agent can call it."""
    seen = {}

    def on_call(context, _dispatch):
        seen["run_id"] = context.run_id
        seen["turn_id"] = context.turn_id
        seen["prompt_id"] = context.prompt_id

    _fake_agent(monkeypatch, on_call=on_call)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=True)
    _drain()

    assert seen["run_id"] is not None
    assert seen["turn_id"] == turn.turn_id
    assert seen["prompt_id"] == "prompt_v1"


def test_a_proposal_made_during_a_run_lands_on_that_run(seeded, monkeypatch):
    """End to end through the executor: the agent calls its tool mid-run."""
    def on_call(context, dispatch_fn):
        result = dispatch_fn(
            admin_tools.TOOL_NAME,
            {"new_prompt_text": "a revised prompt. " + ("filler text. " * 20),
             "rationale": "it over-cited"},
            context,
        )
        assert result["status"] == "proposed", result

    _fake_agent(monkeypatch, on_call=on_call)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=True)
    _drain()

    pending = conversations.pending_revisions(conv.conversation_id)
    assert len(pending) == 1
    assert pending[0]["source_turn_id"] == turn.turn_id
    assert pending[0]["source_run_id"] == conversations.active_run(turn.turn_id)["run_id"]


def test_regeneration_replaces_the_answer_and_keeps_one_query(seeded, monkeypatch):
    _fake_agent(monkeypatch, answer="original answer")
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=True)
    _drain()

    versions.save_prompt("prompt_v1", "a revised prompt text", "test")
    _fake_agent(monkeypatch, answer="regenerated answer")
    runs.enqueue_regenerate(conv.conversation_id, turn.turn_id, "prompt_v2",
                            is_admin=True)
    _drain()

    assert len(conversations.turns_for(conv.conversation_id)) == 1
    responses = conversations.responses_for(turn.turn_id)
    assert [r["revision_index"] for r in responses] == [2, 1]
    assert conversations.active_run(turn.turn_id)["answer"] == "regenerated answer"
    assert conversations.active_run(turn.turn_id)["prompt_id"] == "prompt_v2"

    # History carries the new answer and the question exactly once.
    history = conversations.history_for(conv.conversation_id)
    contents = [m["content"] for m in history]
    assert contents.count("the question") == 1
    assert "regenerated answer" in contents
    assert "original answer" not in contents


def test_regeneration_does_not_see_the_answer_it_replaces(seeded, monkeypatch):
    record = []
    _fake_agent(monkeypatch, answer="answer one", record=record)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "only question")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=True)
    _drain()

    runs.enqueue_regenerate(conv.conversation_id, turn.turn_id, "prompt_v1",
                            is_admin=True)
    _drain()

    assert record[1]["history"] == []


def test_regeneration_flags_later_turns_stale(seeded, monkeypatch):
    _fake_agent(monkeypatch)
    conv = conversations.create("admin")
    first = conversations.add_turn(conv.conversation_id, "first")
    runs.enqueue_turn(conv.conversation_id, first.turn_id, "prompt_v1", is_admin=True)
    _drain()
    second = conversations.add_turn(conv.conversation_id, "second")
    runs.enqueue_turn(conv.conversation_id, second.turn_id, "prompt_v1", is_admin=True)
    _drain()

    runs.enqueue_regenerate(conv.conversation_id, first.turn_id, "prompt_v1",
                            is_admin=True)
    _drain()

    stale = {t.turn_index: t.stale for t in conversations.turns_for(conv.conversation_id)}
    assert stale == {1: False, 2: True}


def test_a_failing_agent_fails_the_task_without_losing_the_turn(seeded, monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("model exploded")

    monkeypatch.setattr("harness.runner.agent_run", boom)
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "q")
    runs.enqueue_turn(conv.conversation_id, turn.turn_id, "prompt_v1", is_admin=False)

    finished = _drain()
    assert finished[0]["status"] == "failed"
    assert "model exploded" in finished[0]["error"]
    # The turn survives with no answer, so the transcript can show it pending.
    assert conversations.load_turn(turn.turn_id).query == "q"
    assert conversations.active_run(turn.turn_id) is None
