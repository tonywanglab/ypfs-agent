"""Fixtures for the chat feature tests.

The chat tables are an opt-in addition, so the shared `pg` fixture (which only
applies schema.sql) deliberately does not create them. `chat_pg` layers the chat
DDL on top of that per-test schema — the same two-step an operator runs:
`python db.py --init` then `python -m harness chat-init`.
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def chat_pg(pg):
    """Per-test schema with both the harness and the chat tables."""
    from harness.chat import schema as chat_schema

    chat_schema.init_chat_schema()
    return pg


@pytest.fixture()
def seeded(chat_pg):
    """chat_pg plus the seeded cases and prompt_v1 baseline."""
    from harness import seed

    seed.seed_all()
    return chat_pg


@pytest.fixture()
def make_chat_run(seeded):
    """Factory: attach a finished run + answer to a turn, bypassing the agent.

    Returns the run_id. Mirrors tests/conftest.py's make_run, but links the run
    to a chat turn at the next revision_index so the transcript and history code
    have something real to read.
    """
    from harness import dbio
    from harness.models import Case, RunManifest
    from harness.runner import save_manifest
    from harness.seed import insert_case
    from harness.chat import conversations

    counter = {"n": 0}

    def _make(turn_id, answer="an answer", prompt_id="prompt_v1", trace=None,
              created_at=None):
        counter["n"] += 1
        run_id = f"run_{counter['n']:012x}"
        case_id = f"chat_case_{counter['n']}"
        insert_case(Case(case_id=case_id, prompt="composed question"), adhoc=True)
        save_manifest(
            RunManifest(
                run_id=run_id,
                case_id=case_id,
                agent_model="test-agent",
                prompt_id=prompt_id,
                created_at=created_at or f"2024-01-01T00:00:{counter['n']:02d}Z",
                status="complete",
                sample_count=1,
            ),
            case_snapshot={"case_id": case_id, "prompt": "composed question",
                           "tags": [], "notes": ""},
        )
        dbio.execute(
            "INSERT INTO run_samples (run_id, sample_index, answer, trace) "
            "VALUES (%s, %s, %s, %s)",
            (run_id, conversations.CHAT_SAMPLE_INDEX, answer,
             dbio.jsonb(trace if trace is not None else {"messages": [], "normalized": {}})),
        )
        conversations.link_run(run_id, turn_id,
                              conversations.next_revision_index(turn_id))
        return run_id

    return _make
