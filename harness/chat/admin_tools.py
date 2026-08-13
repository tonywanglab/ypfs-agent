"""The admin-only agent tool: propose a system-prompt revision.

This is what makes "the agent changes the system prompt" real. In an admin
conversation the agent is handed one extra tool, so when the exchange implies a
prompt-level problem — not a wrong fact, but a wrong instruction — it can say so
in the one form that persists: a concrete revision of its own system prompt.

Two boundaries are deliberate:

* The tool only ever writes `status='proposed'`. Committing goes through
  versions.save_prompt() when an admin clicks Accept, so the agent can suggest
  but never rewrite its own instructions unattended.
* The tool is absent from the schema list on non-admin runs, so a user-role
  agent cannot call it — there is nothing to call. The is_admin check below is
  defense in depth, not the gate.
"""

from __future__ import annotations

from agent import tools as agent_tools

from .. import dbio
from ..storage import now_iso
from . import ids

TOOL_NAME = "propose_system_prompt_revision"

# Guardrails on the proposal, checked before the row is written. A draft that
# fails these is refused with a message the model can read and retry against,
# rather than becoming a proposal an admin has to notice is broken.
MIN_TEXT_CHARS = 200
MAX_GROWTH_FACTOR = 3.0

SCHEMA = {
    "type": "function",
    "function": {
        "name": TOOL_NAME,
        "description": (
            "Propose a revision to your own system prompt. Use this when the "
            "conversation reveals a problem with your standing instructions — a "
            "missing constraint, a rule that produced the wrong behavior, an "
            "ambiguity worth resolving — rather than a one-off mistake in this "
            "answer. Supply the COMPLETE revised prompt text, not a diff or a "
            "fragment: it replaces the current prompt wholesale. Preserve the "
            "instructions that are working; change only what the conversation "
            "shows is wrong. The proposal is shown to a human for approval and "
            "takes effect only if they accept it, so explain your reasoning in "
            "`rationale`. Propose at most one revision per response."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "new_prompt_text": {
                    "type": "string",
                    "description": "The complete revised system prompt.",
                },
                "rationale": {
                    "type": "string",
                    "description": (
                        "Why this change, tied to what happened in this "
                        "conversation. One or two sentences."
                    ),
                },
            },
            "required": ["new_prompt_text", "rationale"],
        },
    },
}


def propose_system_prompt_revision(new_prompt_text: str = "", rationale: str = "",
                                  *, context) -> dict:
    """Write a proposed revision for the admin to accept or dismiss.

    Returns a dict either way — the agent tool contract is that a failure is
    readable data, not an exception.
    """
    if not getattr(context, "is_admin", False):
        return {"error": "not_available: this tool requires an admin conversation"}

    conversation_id = getattr(context, "conversation_id", None)
    from_prompt_id = getattr(context, "prompt_id", None)
    if not conversation_id or not from_prompt_id:
        return {"error": "not_available: no conversation context for this run"}

    text = (new_prompt_text or "").strip()
    if not text:
        return {"error": "new_prompt_text was empty; supply the complete revised prompt"}
    if len(text) < MIN_TEXT_CHARS:
        return {
            "error": (
                f"new_prompt_text is only {len(text)} characters. Supply the COMPLETE "
                f"revised system prompt (at least {MIN_TEXT_CHARS} characters), not a "
                "fragment or a description of the change."
            )
        }

    current = dbio.q1(
        "SELECT text FROM prompt_versions WHERE prompt_id = %s", (from_prompt_id,)
    )
    if current is None:
        return {"error": f"not_available: unknown prompt version {from_prompt_id}"}
    baseline = len(current["text"])
    if baseline and len(text) > baseline * MAX_GROWTH_FACTOR:
        return {
            "error": (
                f"new_prompt_text is {len(text)} characters against a "
                f"{baseline}-character current prompt. Revise the existing prompt "
                "rather than writing a much longer new one."
            )
        }

    revision_id = ids.new("revision")
    dbio.execute(
        """
        INSERT INTO chat_prompt_revisions
            (revision_id, conversation_id, source_turn_id, source_run_id,
             from_prompt_id, proposed_text, rationale, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'proposed', %s)
        """,
        (revision_id, conversation_id, getattr(context, "turn_id", None),
         getattr(context, "run_id", None), from_prompt_id, text,
         (rationale or "").strip(), now_iso()),
    )
    return {
        "status": "proposed",
        "revision_id": revision_id,
        "from_prompt_id": from_prompt_id,
        "note": (
            "Proposal recorded and shown to the admin for approval. It is not in "
            "effect yet. Tell them plainly what you changed and why."
        ),
    }


def dispatch(name: str, args: dict, context=None) -> dict:
    """Tool dispatch for admin chat runs: this package's one tool, then the
    agent's own registry for everything else.

    Same never-raises contract as agent.tools.dispatch — a failure has to reach
    the model as readable data or the loop dies mid-conversation.
    """
    if name != TOOL_NAME:
        return agent_tools.dispatch(name, args, context)
    try:
        return propose_system_prompt_revision(context=context, **args)
    except (Exception, SystemExit) as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def agent_kwargs() -> dict:
    """The tools/dispatch_fn pair for an admin run.

    A fresh list each call: never mutate agent_tools.TOOLS, or the extra tool
    would leak into every other run in the process.
    """
    return {
        "tools": [*agent_tools.TOOLS, SCHEMA],
        "dispatch_fn": dispatch,
    }
