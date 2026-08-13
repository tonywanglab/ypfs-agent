"""Executing a chat turn.

Wraps runner.run_case_samples() rather than reimplementing it: a chat turn is
one single-sample run, persisted the same way every other run is, so it shows up
in the existing runs list and trace viewer for free. What this module adds on top
is conversational history, the admin tool seam, and the chat_run_links row that
attaches the resulting run to its turn.

Both task kinds go through one code path — regenerating a turn is the same work
as answering it, just at a higher revision_index against a newer prompt.
"""

from __future__ import annotations

from agent.context import RunContext

from .. import tasks, versions
from ..models import Case
from ..runner import run_case_samples
from ..storage import new_id
from . import admin_tools, conversations


def enqueue_turn(conversation_id: str, turn_id: str, prompt_id: str, is_admin: bool,
                 kind: str = tasks.KIND_CHAT_TURN, task_id: str | None = None) -> dict:
    return tasks.enqueue(
        kind,
        payload={
            "conversation_id": conversation_id,
            "turn_id": turn_id,
            "prompt_id": prompt_id,
            "is_admin": bool(is_admin),
        },
        task_id=task_id,
    )


def enqueue_regenerate(conversation_id: str, turn_id: str, prompt_id: str,
                       is_admin: bool, task_id: str | None = None) -> dict:
    return enqueue_turn(conversation_id, turn_id, prompt_id, is_admin,
                        kind=tasks.KIND_CHAT_REGENERATE, task_id=task_id)


def _execute(task: dict) -> None:
    payload = task["payload"]
    conversation_id = payload["conversation_id"]
    turn_id = payload["turn_id"]
    is_admin = bool(payload.get("is_admin"))
    task_id = task["task_id"]

    turn = conversations.load_turn(turn_id)
    prompt = versions.load_prompt(payload["prompt_id"])

    # Only turns BEFORE this one: a regeneration must not see the answer it is
    # replacing, and the live turn's own question is the user message.
    history = conversations.history_for(conversation_id,
                                       before_turn_index=turn.turn_index)
    revision_index = conversations.next_revision_index(turn_id)

    # case.prompt is the user message the agent receives, so it is the composed
    # text (quote + typed question) — which also means the run's case_snapshot
    # records exactly what was asked.
    case = Case(
        case_id=new_id("chat"),
        prompt=conversations.compose_message(turn),
        tags=["chat", "admin" if is_admin else "user"],
        notes=f"conversation={conversation_id} turn={turn_id} revision={revision_index}",
    )

    context = RunContext(
        conversation_id=conversation_id,
        turn_id=turn_id,
        prompt_id=prompt.prompt_id,
        is_admin=is_admin,
    )
    # The admin tool needs a run_id to attach a proposal to, and run_id isn't
    # known until run_case_samples mints it — on_progress('prepare') is the
    # first moment it exists, which is before the agent call.
    agent_kwargs = admin_tools.agent_kwargs() if is_admin else None

    def on_progress(phase, sample_index, sample_total, run_id):
        if run_id:
            context.run_id = run_id
            tasks.set_run(task_id, run_id)
            conversations.link_run(run_id, turn_id, revision_index)
        tasks.set_progress(
            task_id,
            phase=phase,
            turn_id=turn_id,
            revision_index=revision_index,
            message={
                "prepare": "Preparing…",
                "agent": "Thinking…",
                "sample_done": "Finishing…",
            }.get(phase, "Working…"),
        )

    manifest = run_case_samples(
        case,
        prompt.text,
        prompt.prompt_id,
        samples=1,
        on_progress=on_progress,
        context=context,
        history=history,
        agent_kwargs=agent_kwargs,
    )
    conversations.link_run(manifest.run_id, turn_id, revision_index)

    if revision_index > 1:
        # A regenerated answer invalidates the turns that followed it. Flag them
        # instead of silently re-running work nobody asked to change.
        conversations.mark_downstream_stale(turn_id)
    else:
        _title_from_first_turn(conversation_id, turn)

    tasks.finish(task_id, result={
        "run_id": manifest.run_id,
        "turn_id": turn_id,
        "conversation_id": conversation_id,
        "revision_index": revision_index,
    })


def _title_from_first_turn(conversation_id: str, turn) -> None:
    """Name an untitled conversation after its opening question."""
    if turn.turn_index != 1:
        return
    conversation = conversations.load(conversation_id)
    if conversation.title:
        return
    conversations.set_title(conversation_id, conversations.derive_title(turn.query))


def register_executors(executors: dict) -> None:
    """Attach the chat task kinds to a worker's executor table.

    Called from harness/worker.py behind a guarded import, so deleting this
    package leaves the worker running with two fewer kinds rather than broken.
    """
    executors[tasks.KIND_CHAT_TURN] = _execute
    executors[tasks.KIND_CHAT_REGENERATE] = _execute
