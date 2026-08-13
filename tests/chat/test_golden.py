"""Golden pairs: admin-only marking, snapshot semantics, and the viewer page."""

from __future__ import annotations

import pytest

from harness import versions, web
from harness.chat import conversations, golden


def _admin_client(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setenv("HARNESS_ADMIN_PASSWORD", "pw")
    client = web.create_app().test_client()
    assert client.post("/login", data={"password": "pw"}).status_code == 302
    return client


def _user_client(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setenv("HARNESS_ADMIN_PASSWORD", "pw")
    return web.create_app().test_client()


# ---- Marking --------------------------------------------------------------

def test_mark_snapshots_the_query_and_answer(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "what caused the run?")
    run_id = make_chat_run(turn.turn_id, answer="Deposit flight did.")

    pair = golden.mark(turn.turn_id, run_id, note="good synthesis")

    assert pair.query == "what caused the run?"
    assert pair.answer == "Deposit flight did."
    assert pair.prompt_id == "prompt_v1"
    assert pair.note == "good synthesis"
    assert golden.for_run(run_id) is not None


def test_marked_query_includes_the_quoted_span(seeded, make_chat_run):
    """A judge has to see the same input the answer was produced from."""
    conv = conversations.create("admin")
    first = conversations.add_turn(conv.conversation_id, "first")
    first_run = make_chat_run(first.turn_id, answer="Bagehot said lend freely.")
    second = conversations.add_turn(
        conv.conversation_id, "expand on that",
        quoted_text="Bagehot said lend freely.", quoted_run_id=first_run,
    )
    second_run = make_chat_run(second.turn_id, answer="Here is more detail.")

    pair = golden.mark(second.turn_id, second_run)
    assert "> Bagehot said lend freely." in pair.query
    assert "expand on that" in pair.query


def test_snapshot_survives_regeneration_of_its_turn(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "the question")
    first_run = make_chat_run(turn.turn_id, answer="the original answer")
    pair = golden.mark(turn.turn_id, first_run)

    # Re-answer the turn: a new revision becomes active.
    make_chat_run(turn.turn_id, answer="a completely different answer")

    assert conversations.active_run(turn.turn_id)["answer"] == "a completely different answer"
    # The saved pair still says what it said when it was marked.
    assert golden.load(pair.golden_id).answer == "the original answer"


def test_marking_is_idempotent_per_response(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    run_id = make_chat_run(turn.turn_id)

    first = golden.mark(turn.turn_id, run_id)
    second = golden.mark(turn.turn_id, run_id)

    assert first.golden_id == second.golden_id
    assert len(golden.list_pairs()) == 1


def test_unmark_removes_the_pair(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    run_id = make_chat_run(turn.turn_id)
    golden.mark(turn.turn_id, run_id)

    assert golden.unmark(run_id) is not None
    assert golden.for_run(run_id) is None
    assert golden.unmark(run_id) is None  # already gone


def test_cannot_mark_a_response_that_belongs_to_another_turn(seeded, make_chat_run):
    conv = conversations.create("admin")
    a = conversations.add_turn(conv.conversation_id, "a")
    b = conversations.add_turn(conv.conversation_id, "b")
    a_run = make_chat_run(a.turn_id)
    make_chat_run(b.turn_id)

    with pytest.raises(FileNotFoundError):
        golden.mark(b.turn_id, a_run)


def test_cannot_mark_a_run_with_no_answer(seeded):
    from harness.models import Case, RunManifest
    from harness.runner import save_manifest
    from harness.seed import insert_case

    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    insert_case(Case(case_id="pending_case", prompt="q"), adhoc=True)
    save_manifest(
        RunManifest("run_aaaaaaaaaaaa", "pending_case", "m", "prompt_v1",
                    "2024-01-01T00:00:00Z", status="pending", sample_count=1),
        case_snapshot={"case_id": "pending_case", "prompt": "q", "tags": [], "notes": ""},
    )
    conversations.link_run("run_aaaaaaaaaaaa", turn.turn_id, 1)

    with pytest.raises(ValueError):
        golden.mark(turn.turn_id, "run_aaaaaaaaaaaa")


def test_marked_run_ids_answers_in_one_query(seeded, make_chat_run):
    conv = conversations.create("admin")
    t1 = conversations.add_turn(conv.conversation_id, "a")
    t2 = conversations.add_turn(conv.conversation_id, "b")
    r1 = make_chat_run(t1.turn_id)
    r2 = make_chat_run(t2.turn_id)
    golden.mark(t1.turn_id, r1)

    assert golden.marked_run_ids([r1, r2]) == {r1}
    assert golden.marked_run_ids([]) == set()


def test_list_filters_by_prompt_version(seeded, make_chat_run):
    versions.save_prompt("prompt_v1", "a second version of the prompt", "test")
    conv = conversations.create("admin")
    t1 = conversations.add_turn(conv.conversation_id, "old")
    t2 = conversations.add_turn(conv.conversation_id, "new")
    golden.mark(t1.turn_id, make_chat_run(t1.turn_id, prompt_id="prompt_v1"))
    golden.mark(t2.turn_id, make_chat_run(t2.turn_id, prompt_id="prompt_v2"))

    assert len(golden.list_pairs()) == 2
    assert [p.prompt_id for p in golden.list_pairs("prompt_v2")] == ["prompt_v2"]
    assert golden.prompt_ids_with_pairs() == ["prompt_v1", "prompt_v2"]


# ---- Routes ---------------------------------------------------------------

def test_star_toggles_through_the_route(seeded, monkeypatch, make_chat_run):
    client = _admin_client(monkeypatch)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    run_id = make_chat_run(turn.turn_id, answer="an answer")
    form = {"conversation_id": conv.conversation_id, "turn_id": turn.turn_id,
            "run_id": run_id}

    client.post("/golden/mark", data=form)
    assert golden.for_run(run_id) is not None
    client.post("/golden/mark", data=form)
    assert golden.for_run(run_id) is None


def test_golden_page_lists_pairs_and_links_back(seeded, monkeypatch, make_chat_run):
    client = _admin_client(monkeypatch)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "a distinctive question")
    run_id = make_chat_run(turn.turn_id, answer="a distinctive answer")
    golden.mark(turn.turn_id, run_id)

    body = client.get("/golden").get_data(as_text=True)
    assert "a distinctive question" in body
    assert "a distinctive answer" in body
    assert conv.conversation_id in body


def test_golden_page_delete(seeded, monkeypatch, make_chat_run):
    client = _admin_client(monkeypatch)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    pair = golden.mark(turn.turn_id, make_chat_run(turn.turn_id))

    assert client.post(f"/golden/{pair.golden_id}/delete").status_code == 302
    assert golden.list_pairs() == []


def test_users_cannot_mark_or_view_golden_pairs(seeded, monkeypatch, make_chat_run):
    client = _user_client(monkeypatch)
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "q")
    run_id = make_chat_run(turn.turn_id, answer="an answer")

    # Server-side gate, not just a hidden button.
    assert client.post("/golden/mark", data={
        "conversation_id": conv.conversation_id,
        "turn_id": turn.turn_id,
        "run_id": run_id,
    }).status_code == 403
    assert golden.for_run(run_id) is None
    assert client.get("/golden").status_code == 302

    # And the control is absent from the rendered transcript.
    body = client.get(f"/c/{conv.conversation_id}").get_data(as_text=True)
    assert "Mark golden" not in body
    assert "golden-toggle" not in body


def test_admin_sees_the_star_in_the_transcript(seeded, monkeypatch, make_chat_run):
    client = _admin_client(monkeypatch)
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    make_chat_run(turn.turn_id, answer="an answer")

    body = client.get(f"/c/{conv.conversation_id}").get_data(as_text=True)
    assert "Mark golden" in body


def test_deleting_a_conversation_removes_its_pairs(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "q")
    golden.mark(turn.turn_id, make_chat_run(turn.turn_id))

    conversations.delete(conv.conversation_id)
    assert golden.list_pairs() == []
