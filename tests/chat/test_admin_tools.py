"""The admin-only prompt-revision tool, and the accept/dismiss/revert loop."""

from __future__ import annotations

import pytest
from agent.context import RunContext

from harness import tasks, versions, web
from harness.chat import admin_tools, conversations, revisions


def _context(conversation_id, turn_id=None, run_id=None, prompt_id="prompt_v1",
             is_admin=True):
    return RunContext(conversation_id=conversation_id, turn_id=turn_id,
                      run_id=run_id, prompt_id=prompt_id, is_admin=is_admin)


def _long_prompt(marker="revised"):
    return f"{marker} system prompt. " + ("filler instruction text. " * 20)


# ---- Tool availability ----------------------------------------------------

def test_user_runs_never_receive_the_tool():
    """The gate is absence from the schema list, not a runtime check."""
    from agent import tools as agent_tools

    names = [t["function"]["name"] for t in agent_tools.TOOLS]
    assert admin_tools.TOOL_NAME not in names

    admin_names = [t["function"]["name"] for t in admin_tools.agent_kwargs()["tools"]]
    assert admin_tools.TOOL_NAME in admin_names


def test_agent_kwargs_does_not_mutate_the_shared_registry():
    from agent import tools as agent_tools

    before = len(agent_tools.TOOLS)
    admin_tools.agent_kwargs()
    admin_tools.agent_kwargs()
    assert len(agent_tools.TOOLS) == before


def test_dispatch_delegates_unknown_names_to_the_agent_registry():
    result = admin_tools.dispatch("no_such_tool", {}, RunContext())
    assert "unknown tool" in result["error"]


def test_tool_refuses_a_non_admin_context(seeded):
    conv = conversations.create("user")
    result = admin_tools.propose_system_prompt_revision(
        new_prompt_text=_long_prompt(), rationale="why",
        context=_context(conv.conversation_id, is_admin=False),
    )
    assert "not_available" in result["error"]
    assert conversations.pending_revisions(conv.conversation_id) == []


# ---- Proposal validation --------------------------------------------------

def test_tool_writes_a_proposal_without_touching_prompt_versions(seeded):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    before = [p.prompt_id for p in versions.list_prompts()]

    result = admin_tools.propose_system_prompt_revision(
        new_prompt_text=_long_prompt(), rationale="over-cited a primary source",
        context=_context(conv.conversation_id, turn_id=turn.turn_id),
    )

    assert result["status"] == "proposed"
    pending = conversations.pending_revisions(conv.conversation_id)
    assert len(pending) == 1
    assert pending[0]["status"] == "proposed"
    assert pending[0]["to_prompt_id"] is None
    assert pending[0]["source_turn_id"] == turn.turn_id
    # The agent proposed; it did not commit.
    assert [p.prompt_id for p in versions.list_prompts()] == before


def test_tool_rejects_a_fragment_instead_of_a_full_prompt(seeded):
    conv = conversations.create("admin")
    result = admin_tools.propose_system_prompt_revision(
        new_prompt_text="add a rule about citations", rationale="why",
        context=_context(conv.conversation_id),
    )
    assert "COMPLETE" in result["error"]
    assert conversations.pending_revisions(conv.conversation_id) == []


def test_tool_rejects_an_empty_proposal(seeded):
    conv = conversations.create("admin")
    result = admin_tools.propose_system_prompt_revision(
        new_prompt_text="   ", rationale="why",
        context=_context(conv.conversation_id),
    )
    assert "empty" in result["error"]


def test_tool_rejects_a_runaway_rewrite(seeded):
    conv = conversations.create("admin")
    baseline = len(versions.load_prompt("prompt_v1").text)
    result = admin_tools.propose_system_prompt_revision(
        new_prompt_text="x" * int(baseline * admin_tools.MAX_GROWTH_FACTOR + 100),
        rationale="why",
        context=_context(conv.conversation_id),
    )
    assert "much longer" in result["error"]
    assert conversations.pending_revisions(conv.conversation_id) == []


def test_dispatch_turns_a_bad_argument_into_readable_data(seeded):
    """A malformed tool call must not kill the agent loop mid-conversation."""
    conv = conversations.create("admin")
    result = admin_tools.dispatch(
        admin_tools.TOOL_NAME, {"bogus_argument": 1},
        _context(conv.conversation_id),
    )
    assert "error" in result


# ---- Accept / dismiss / revert -------------------------------------------

def _propose(conversation_id, turn_id, text=None):
    admin_tools.propose_system_prompt_revision(
        new_prompt_text=text or _long_prompt(), rationale="a reason",
        context=_context(conversation_id, turn_id=turn_id),
    )
    return conversations.pending_revisions(conversation_id)[0]["revision_id"]


def test_accept_saves_a_version_and_queues_a_regeneration(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    make_chat_run(turn.turn_id, answer="the first answer")
    revision_id = _propose(conv.conversation_id, turn.turn_id)

    result = revisions.accept(revision_id)

    assert result["prompt"].prompt_id == "prompt_v2"
    assert result["prompt"].parent_prompt_id == "prompt_v1"
    assert versions.latest_prompt_id() == "prompt_v2"

    stored = revisions.load(revision_id)
    assert stored.status == "accepted"
    assert stored.to_prompt_id == "prompt_v2"

    queued = [t for t in tasks.list_active() if t["kind"] == "chat_regenerate"]
    assert len(queued) == 1
    assert queued[0]["payload"]["turn_id"] == turn.turn_id
    assert queued[0]["payload"]["prompt_id"] == "prompt_v2"


def test_accept_is_not_repeatable(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    make_chat_run(turn.turn_id)
    revision_id = _propose(conv.conversation_id, turn.turn_id)

    revisions.accept(revision_id)
    with pytest.raises(ValueError):
        revisions.accept(revision_id)
    # Exactly one new version, not two.
    assert [p.prompt_id for p in versions.list_prompts()] == ["prompt_v1", "prompt_v2"]


def test_dismiss_writes_nothing_but_the_status(seeded):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    revision_id = _propose(conv.conversation_id, turn.turn_id)

    revisions.dismiss(revision_id)

    assert revisions.load(revision_id).status == "dismissed"
    assert [p.prompt_id for p in versions.list_prompts()] == ["prompt_v1"]
    assert conversations.pending_revisions(conv.conversation_id) == []
    assert [t for t in tasks.list_active() if t["kind"] == "chat_regenerate"] == []


def test_revert_appends_a_version_carrying_the_old_text(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    make_chat_run(turn.turn_id)
    original = versions.load_prompt("prompt_v1").text
    revision_id = _propose(conv.conversation_id, turn.turn_id)
    revisions.accept(revision_id)

    reverted = revisions.revert(revision_id)

    assert reverted.prompt_id == "prompt_v3"
    assert reverted.text == original.strip()
    # prompt_v2 is untouched: versions are immutable, undo is append-only.
    assert versions.load_prompt("prompt_v2").text != original.strip()
    assert "Revert" in reverted.rationale


def test_revert_refuses_when_the_prompt_already_matches(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    make_chat_run(turn.turn_id)
    revision_id = _propose(conv.conversation_id, turn.turn_id)
    revisions.accept(revision_id)
    revisions.revert(revision_id)

    with pytest.raises(ValueError):
        revisions.revert(revision_id)


def test_revert_refuses_a_proposal_that_was_never_accepted(seeded):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    revision_id = _propose(conv.conversation_id, turn.turn_id)
    with pytest.raises(ValueError):
        revisions.revert(revision_id)


def test_diff_is_built_against_the_prompt_the_proposal_was_made_on(seeded):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    revision_id = _propose(conv.conversation_id, turn.turn_id,
                           text=_long_prompt("DISTINCTIVE"))
    groups = revisions.diff_for(revisions.load(revision_id))
    added = [row["text"] for group in groups for row in group["rows"]
             if row["kind"] == "add"]
    assert any("DISTINCTIVE" in line for line in added)


# ---- Routes ---------------------------------------------------------------

def _admin_client(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setenv("HARNESS_ADMIN_PASSWORD", "pw")
    client = web.create_app().test_client()
    assert client.post("/login", data={"password": "pw"}).status_code == 302
    return client


def test_proposal_card_renders_in_the_transcript_with_a_diff(seeded, monkeypatch,
                                                             make_chat_run):
    client = _admin_client(monkeypatch)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    make_chat_run(turn.turn_id, answer="an answer")
    _propose(conv.conversation_id, turn.turn_id, text=_long_prompt("DISTINCTIVE"))

    body = client.get(f"/c/{conv.conversation_id}").get_data(as_text=True)
    assert "proposes revising its system prompt" in body
    assert "DISTINCTIVE" in body
    assert "Accept" in body
    assert "Dismiss" in body


def test_accept_route_then_shows_a_revision_event(seeded, monkeypatch, make_chat_run):
    client = _admin_client(monkeypatch)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    make_chat_run(turn.turn_id, answer="an answer")
    revision_id = _propose(conv.conversation_id, turn.turn_id)

    response = client.post(
        f"/c/{conv.conversation_id}/revisions/{revision_id}/accept")
    assert response.status_code == 302

    body = client.get(f"/c/{conv.conversation_id}").get_data(as_text=True)
    assert "System prompt revised" in body
    assert "prompt_v2" in body


def test_revision_routes_are_admin_only(seeded, monkeypatch):
    monkeypatch.setenv("HARNESS_ADMIN_PASSWORD", "pw")
    client = web.create_app().test_client()
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    revision_id = _propose(conv.conversation_id, turn.turn_id)
    url = f"/c/{conv.conversation_id}/revisions/{revision_id}/accept"
    assert client.post(url).status_code == 403
    assert revisions.load(revision_id).status == "proposed"
