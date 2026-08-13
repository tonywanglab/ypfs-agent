"""Accepting, dismissing, and reverting system-prompt revisions.

The agent proposes (admin_tools); an admin decides here. Accepting is the only
path that writes a prompt version, and it goes through versions.save_prompt() —
the same append-only, immutable, parent-linked allocation the eval harness uses.
Nothing here mutates an existing prompt_vN, so "revert" is also just another
save: a new version carrying an older version's text.
"""

from __future__ import annotations

from .. import dbio, versions
from ..text_diff import build_line_diff
from . import runs
from .models import PromptRevision

STATUS_PROPOSED = "proposed"
STATUS_ACCEPTED = "accepted"
STATUS_DISMISSED = "dismissed"


def _from_row(row: dict) -> PromptRevision:
    return PromptRevision.from_dict(row)


def load(revision_id: str) -> PromptRevision:
    row = dbio.q1(
        "SELECT * FROM chat_prompt_revisions WHERE revision_id = %s", (revision_id,)
    )
    if row is None:
        raise FileNotFoundError(f"Revision {revision_id!r} does not exist")
    return _from_row(row)


def diff_for(revision: PromptRevision) -> list[dict]:
    """Line diff from the prompt the proposal was made against to the proposal.

    Reuses the harness's existing diff builder, so the card in the transcript
    renders with the same markup as the prompt-draft review page.
    """
    base = versions.load_prompt(revision.from_prompt_id)
    return build_line_diff(base.text, revision.proposed_text)


def accept(revision_id: str, is_admin_conversation: bool = True) -> dict:
    """Commit a proposal as the next prompt version and re-answer its turn.

    Ordering matters: save the version first, then record acceptance, then queue
    the regeneration. If the save fails nothing is marked accepted, and the
    proposal is still there to retry.
    """
    revision = load(revision_id)
    if revision.status != STATUS_PROPOSED:
        raise ValueError(f"Revision {revision_id} is already {revision.status}")

    prompt = versions.save_prompt(
        base_prompt_id=revision.from_prompt_id,
        text=revision.proposed_text,
        rationale=revision.rationale or f"Accepted proposal {revision_id}",
    )
    dbio.execute(
        """
        UPDATE chat_prompt_revisions
           SET status = %s, to_prompt_id = %s
         WHERE revision_id = %s
        """,
        (STATUS_ACCEPTED, prompt.prompt_id, revision_id),
    )

    # Re-answer the turn that prompted the change, under the new prompt. That is
    # what makes the edit visible: same question, better instructions.
    task = None
    if revision.source_turn_id:
        task = runs.enqueue_regenerate(
            conversation_id=revision.conversation_id,
            turn_id=revision.source_turn_id,
            prompt_id=prompt.prompt_id,
            is_admin=is_admin_conversation,
        )
    return {"prompt": prompt, "task": task, "revision": load(revision_id)}


def dismiss(revision_id: str) -> PromptRevision:
    """Reject a proposal. Writes nothing but the status."""
    revision = load(revision_id)
    if revision.status != STATUS_PROPOSED:
        raise ValueError(f"Revision {revision_id} is already {revision.status}")
    dbio.execute(
        "UPDATE chat_prompt_revisions SET status = %s WHERE revision_id = %s",
        (STATUS_DISMISSED, revision_id),
    )
    return load(revision_id)


def revert(revision_id: str) -> object:
    """Undo an accepted revision by saving a NEW version with the old text.

    Prompt versions are immutable, so undo is append-only too: prompt_v4 that
    reverts prompt_v3 carries prompt_v2's text and records why. The accepted
    revision row is left alone — it happened, and the history should say so.
    """
    revision = load(revision_id)
    if revision.status != STATUS_ACCEPTED:
        raise ValueError(f"Revision {revision_id} was never accepted")
    base = versions.load_prompt(revision.from_prompt_id)
    latest = versions.latest_prompt()
    if latest.text == base.text:
        raise ValueError("The current prompt already matches that text")
    return versions.save_prompt(
        base_prompt_id=latest.prompt_id,
        text=base.text,
        rationale=(
            f"Revert of {revision.to_prompt_id or revision_id}: "
            f"restores {base.prompt_id} text."
        ),
    )
