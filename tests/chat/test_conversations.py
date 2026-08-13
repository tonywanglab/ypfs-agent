from __future__ import annotations

import pytest

from harness.chat import conversations


def test_chat_init_is_idempotent(chat_pg):
    from harness.chat import schema as chat_schema

    assert chat_schema.is_installed()
    chat_schema.init_chat_schema()  # again
    assert len(chat_schema.installed_tables()) == len(chat_schema.CHAT_TABLES)


def test_turns_are_appended_with_increasing_index(chat_pg):
    conv = conversations.create("user")
    first = conversations.add_turn(conv.conversation_id, "one")
    second = conversations.add_turn(conv.conversation_id, "two")
    assert (first.turn_index, second.turn_index) == (1, 2)
    assert [t.query for t in conversations.turns_for(conv.conversation_id)] == ["one", "two"]


def test_add_turn_rejects_empty_query(chat_pg):
    conv = conversations.create("user")
    with pytest.raises(ValueError):
        conversations.add_turn(conv.conversation_id, "   ")


def test_compose_message_keeps_query_and_quote_separate(chat_pg):
    conv = conversations.create("admin")
    turn = conversations.add_turn(
        conv.conversation_id,
        "this over-cites a primary source",
        quoted_text="Bagehot argued for lending freely.",
    )
    # Stored: only what was typed.
    assert turn.query == "this over-cites a primary source"
    assert turn.quoted_text == "Bagehot argued for lending freely."
    # Sent to the model: both, with the span as a blockquote.
    composed = conversations.compose_message(turn)
    assert "> Bagehot argued for lending freely." in composed
    assert composed.endswith("this over-cites a primary source")


def test_compose_message_without_a_quote_is_the_bare_query(chat_pg):
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "what happened in 2008?")
    assert conversations.compose_message(turn) == "what happened in 2008?"


def test_regeneration_adds_a_revision_not_a_turn(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "question")
    first = make_chat_run(turn.turn_id, answer="first answer")
    second = make_chat_run(turn.turn_id, answer="second answer", prompt_id="prompt_v1")

    assert len(conversations.turns_for(conv.conversation_id)) == 1
    revisions = conversations.responses_for(turn.turn_id)
    assert [r["revision_index"] for r in revisions] == [2, 1]
    active = conversations.active_run(turn.turn_id)
    assert active["run_id"] == second
    assert active["answer"] == "second answer"
    assert first != second


def test_active_run_skips_a_revision_that_never_produced_an_answer(seeded, make_chat_run):
    """A crashed regeneration must not blank out a turn that already answered."""
    from harness import dbio
    from harness.models import Case, RunManifest
    from harness.runner import save_manifest
    from harness.seed import insert_case

    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "question")
    good = make_chat_run(turn.turn_id, answer="the good answer")

    insert_case(Case(case_id="crashed_case", prompt="q"), adhoc=True)
    save_manifest(
        RunManifest("run_ffffffffffff", "crashed_case", "test-agent", "prompt_v1",
                    "2024-06-01T00:00:00Z", status="pending", sample_count=1),
        case_snapshot={"case_id": "crashed_case", "prompt": "q", "tags": [], "notes": ""},
    )
    conversations.link_run("run_ffffffffffff", turn.turn_id,
                          conversations.next_revision_index(turn.turn_id))

    active = conversations.active_run(turn.turn_id)
    assert active["run_id"] == good


def test_history_replays_only_active_revisions(seeded, make_chat_run):
    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "first question")
    make_chat_run(turn.turn_id, answer="stale answer", trace={
        "messages": [{"role": "user", "content": "first question"},
                      {"role": "assistant", "content": "stale answer"}],
    })
    make_chat_run(turn.turn_id, answer="fresh answer", trace={
        "messages": [{"role": "user", "content": "first question"},
                      {"role": "assistant", "content": "fresh answer"}],
    })

    history = conversations.history_for(conv.conversation_id)
    contents = [m.get("content") for m in history]
    assert "fresh answer" in contents
    assert "stale answer" not in contents
    # The query appears exactly once even though there are two responses.
    assert contents.count("first question") == 1


def test_history_before_turn_index_excludes_the_turn_being_answered(seeded, make_chat_run):
    conv = conversations.create("user")
    t1 = conversations.add_turn(conv.conversation_id, "q1")
    make_chat_run(t1.turn_id, answer="a1", trace={
        "messages": [{"role": "user", "content": "q1"},
                      {"role": "assistant", "content": "a1"}],
    })
    t2 = conversations.add_turn(conv.conversation_id, "q2")
    make_chat_run(t2.turn_id, answer="a2", trace={
        "messages": [{"role": "user", "content": "q2"},
                      {"role": "assistant", "content": "a2"}],
    })

    history = conversations.history_for(conv.conversation_id,
                                       before_turn_index=t2.turn_index)
    contents = [m.get("content") for m in history]
    assert contents == ["q1", "a1"]


def test_history_skips_unanswered_turns(seeded, make_chat_run):
    """A turn still running must not leave a dangling user message in history."""
    conv = conversations.create("user")
    t1 = conversations.add_turn(conv.conversation_id, "answered")
    make_chat_run(t1.turn_id, answer="yes", trace={
        "messages": [{"role": "user", "content": "answered"},
                      {"role": "assistant", "content": "yes"}],
    })
    conversations.add_turn(conv.conversation_id, "still running")

    history = conversations.history_for(conv.conversation_id)
    assert [m.get("content") for m in history] == ["answered", "yes"]


def test_history_falls_back_to_question_answer_without_a_trace(seeded, make_chat_run):
    conv = conversations.create("user")
    turn = conversations.add_turn(conv.conversation_id, "no trace here")
    make_chat_run(turn.turn_id, answer="but an answer", trace={"messages": []})

    history = conversations.history_for(conv.conversation_id)
    assert history == [
        {"role": "user", "content": "no trace here"},
        {"role": "assistant", "content": "but an answer"},
    ]


def test_mark_downstream_stale_flags_only_later_turns(chat_pg):
    conv = conversations.create("admin")
    t1 = conversations.add_turn(conv.conversation_id, "one")
    t2 = conversations.add_turn(conv.conversation_id, "two")
    t3 = conversations.add_turn(conv.conversation_id, "three")

    flagged = conversations.mark_downstream_stale(t2.turn_id)
    assert flagged == 1

    stale = {t.turn_id: t.stale for t in conversations.turns_for(conv.conversation_id)}
    assert stale == {t1.turn_id: False, t2.turn_id: False, t3.turn_id: True}


def test_list_for_role_hides_admin_threads_from_users(chat_pg):
    conversations.create("user", title="user thread")
    conversations.create("admin", title="admin thread")

    user_titles = [c.title for c in conversations.list_for_role("user")]
    admin_titles = [c.title for c in conversations.list_for_role("admin")]
    assert user_titles == ["user thread"]
    assert sorted(admin_titles) == ["admin thread", "user thread"]


def test_timeline_orders_turns_and_accepted_revisions(seeded, make_chat_run):
    from harness import dbio
    from harness.chat import ids

    conv = conversations.create("admin")
    turn = conversations.add_turn(conv.conversation_id, "question")
    make_chat_run(turn.turn_id, answer="answer", created_at="2024-01-01T00:00:01Z")

    # Same timestamp as the turn it came from: a revision always renders after
    # its own turn, which is what the sort_key tie-break exists for.
    dbio.execute(
        """
        INSERT INTO chat_prompt_revisions
            (revision_id, conversation_id, source_turn_id, from_prompt_id,
             to_prompt_id, proposed_text, rationale, status, created_at)
        VALUES (%s, %s, %s, 'prompt_v1', 'prompt_v1', 'text', 'why',
                'accepted', %s)
        """,
        (ids.new("revision"), conv.conversation_id, turn.turn_id, turn.created_at),
    )
    # A proposal still awaiting a decision is NOT a transcript event yet.
    dbio.execute(
        """
        INSERT INTO chat_prompt_revisions
            (revision_id, conversation_id, source_turn_id, from_prompt_id,
             proposed_text, rationale, status, created_at)
        VALUES (%s, %s, %s, 'prompt_v1', 'text', 'why', 'proposed', %s)
        """,
        (ids.new("revision"), conv.conversation_id, turn.turn_id, turn.created_at),
    )

    events = conversations.timeline(conv.conversation_id)
    assert [e["kind"] for e in events] == ["turn", "prompt_revision"]
    assert events[0]["active"]["answer"] == "answer"
    assert len(conversations.pending_revisions(conv.conversation_id)) == 1


def test_title_derives_from_the_opening_question():
    assert conversations.derive_title("short one") == "short one"
    long_q = " ".join(f"w{i}" for i in range(20))
    assert conversations.derive_title(long_q).endswith("…")
    assert conversations.derive_title("") == "Untitled"
