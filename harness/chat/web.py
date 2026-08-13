"""Flask blueprint for the chat UI.

Mounted from harness/web.py's create_app() with one register_blueprint() call,
so the feature detaches cleanly. The routes listed in auth.USER_ENDPOINTS are
the only surface an anonymous `user` role can reach; auth.install_guards()
default-denies everything else, including every route in this file that isn't on
that list (golden pairs, prompt revisions).
"""

from __future__ import annotations

from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for)

from .. import dbio, tasks, versions
from ..trace import trace_timeline
from . import auth, conversations, golden, ids, revisions, runs, schema

bp = Blueprint("chat", __name__, template_folder="../templates/chat")


def _require_schema():
    """Fail with an actionable message instead of a raw UndefinedTable error."""
    if not schema.is_installed():
        abort(503, description="Chat tables are missing. Run: python -m harness chat-init")


def _conversation_or_404(conversation_id: str):
    if not ids.valid("conversation", conversation_id):
        abort(404)
    try:
        conversation = conversations.load(conversation_id)
    except FileNotFoundError:
        abort(404)
    # Users must not read admin threads even by guessing an id.
    if conversation.role == "admin" and not auth.is_admin():
        abort(404)
    return conversation


def _prompt_for_next_turn() -> str:
    """Conversations always run against the newest prompt version, never pinned
    to the one they started on — so accepting a revision changes the very next
    message in the same thread."""
    return versions.latest_prompt_id()


# ---- Session / role -------------------------------------------------------

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Password gate for the admin role. GET renders the form; POST checks it.

    Renders a plain "not configured" state when HARNESS_ADMIN_PASSWORD is unset,
    so a blank password can never be accepted.
    """
    next_url = request.values.get("next", "")
    if request.method == "GET":
        return render_template("chat/login.html",
                               admin_enabled=auth.admin_enabled(), next_url=next_url)

    if not auth.admin_enabled():
        return render_template("chat/login.html", admin_enabled=False,
                               next_url=next_url), 403
    if not auth.check_password(request.form.get("password", "")):
        return render_template("chat/login.html", admin_enabled=True,
                               next_url=next_url, error="Incorrect password."), 403

    auth.log_in()
    flash("Signed in as admin.", "success")
    # Relative paths only: never bounce to an absolute URL from a form field.
    if next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)
    return redirect(url_for("chat.conversations_list"))


@bp.route("/logout", methods=["POST"])
def logout():
    auth.log_out()
    flash("Signed out.", "success")
    return redirect(url_for("chat.conversations_list"))


# ---- Conversations --------------------------------------------------------

@bp.route("/c")
def conversations_list():
    _require_schema()
    return render_template(
        "chat/conversations.html",
        conversations=conversations.list_for_role(auth.current_role()),
    )


@bp.route("/c", methods=["POST"])
def new_conversation():
    _require_schema()
    conversation = conversations.create(auth.current_role())
    return redirect(url_for("chat.conversation",
                            conversation_id=conversation.conversation_id))


@bp.route("/c/<conversation_id>")
def conversation(conversation_id: str):
    _require_schema()
    conv = _conversation_or_404(conversation_id)
    timeline = conversations.timeline(conversation_id)

    run_ids = [
        response["run_id"]
        for event in timeline if event["kind"] == "turn"
        for response in ([event["active"]] if event["active"] else []) + event["superseded"]
    ]
    is_admin = auth.is_admin()

    # Traces are built per response so each one can be folded under its own
    # answer, including superseded revisions.
    traces = {
        response["run_id"]: trace_timeline(response["trace"])
        for event in timeline if event["kind"] == "turn"
        for response in ([event["active"]] if event["active"] else []) + event["superseded"]
    }

    pending = revisions_with_diffs(conversation_id) if is_admin else []

    # Diffs for the accepted revisions already in the transcript. Admin-only:
    # the diff is system-prompt text, which a user session never sees.
    accepted_diffs = {}
    if is_admin:
        for event in timeline:
            if event["kind"] != "prompt_revision":
                continue
            revision = revisions.load(event["revision"]["revision_id"])
            accepted_diffs[revision.revision_id] = revisions.diff_for(revision)

    return render_template(
        "chat/conversation.html",
        conversation=conv,
        timeline=timeline,
        traces=traces,
        pending_revisions=pending,
        accepted_diffs=accepted_diffs,
        golden_run_ids=golden.marked_run_ids(run_ids) if is_admin else set(),
        active_prompt_id=_prompt_for_next_turn(),
        in_flight=_in_flight_tasks(conversation_id),
    )


def revisions_with_diffs(conversation_id: str) -> list[dict]:
    """Proposals awaiting a decision, each with its rendered line diff."""
    out = []
    for row in conversations.pending_revisions(conversation_id):
        revision = revisions.load(row["revision_id"])
        out.append({"revision": revision, "diff_groups": revisions.diff_for(revision)})
    return out


def _in_flight_tasks(conversation_id: str) -> list[dict]:
    """Queued/running chat tasks for this conversation, so a reload mid-answer
    still shows a pending turn and keeps polling."""
    active = [
        task for task in tasks.list_active()
        if task["kind"] in (tasks.KIND_CHAT_TURN, tasks.KIND_CHAT_REGENERATE)
        and (task["payload"] or {}).get("conversation_id") == conversation_id
    ]
    active.sort(key=lambda task: task["created_at"] or "")
    return active


@bp.route("/c/<conversation_id>/messages", methods=["POST"])
def post_message(conversation_id: str):
    """Add a turn and queue the agent run that answers it.

    `quoted_text` is the span the person had selected when they typed — it
    becomes part of this question (see conversations.compose_message), not an
    annotation on the earlier answer.
    """
    _require_schema()
    conv = _conversation_or_404(conversation_id)

    query = request.form.get("query", "").strip()
    quoted_text = request.form.get("quoted_text", "").strip() or None
    quoted_run_id = request.form.get("quoted_run_id", "").strip() or None
    if quoted_run_id and not dbio.valid_id("run", quoted_run_id):
        quoted_run_id = None
    if not query:
        flash("Enter a message.", "error")
        return redirect(url_for("chat.conversation", conversation_id=conversation_id))

    try:
        prompt_id = _prompt_for_next_turn()
    except FileNotFoundError:
        flash("No prompt versions exist. Run `python -m harness seed` first.", "error")
        return redirect(url_for("chat.conversation", conversation_id=conversation_id))

    turn = conversations.add_turn(conversation_id, query,
                                 quoted_text=quoted_text, quoted_run_id=quoted_run_id)
    runs.enqueue_turn(
        conversation_id=conversation_id,
        turn_id=turn.turn_id,
        prompt_id=prompt_id,
        # The conversation's role decides the toolset, not the current session:
        # an admin reading a user thread must not hand it the prompt-edit tool.
        is_admin=(conv.role == "admin"),
    )
    return redirect(url_for("chat.conversation", conversation_id=conversation_id)
                    + f"#turn-{turn.turn_id}")


@bp.route("/c/<conversation_id>/status")
def turn_status(conversation_id: str):
    """Polling endpoint for the transcript.

    Deliberately NOT the harness's /tasks/<id>/status: that returns the whole
    task payload, which for a chat turn carries the prompt version and would
    leak admin detail to a user session. This returns only what the transcript
    needs to know — is anything still running, and did the turn count change.
    """
    _require_schema()
    _conversation_or_404(conversation_id)
    active = _in_flight_tasks(conversation_id)
    counts = conversations.answer_counts(conversation_id)
    return jsonify({
        "conversation_id": conversation_id,
        "pending": len(active),
        "turns": counts["turns"],
        "answered": counts["answered"],
        # So the client can distinguish "the run failed" from "nothing queued
        # yet" and stop polling with an honest message instead of reloading.
        "failed": _failed_task_count(conversation_id),
        "messages": [
            (task["progress"] or {}).get("message", "Working…") for task in active
        ],
    })


def _failed_task_count(conversation_id: str) -> int:
    row = dbio.q1(
        """
        SELECT count(*) AS n FROM tasks
         WHERE kind = ANY(%s) AND status = 'failed'
           AND payload->>'conversation_id' = %s
        """,
        ([tasks.KIND_CHAT_TURN, tasks.KIND_CHAT_REGENERATE], conversation_id),
    )
    return int(row["n"]) if row else 0


@bp.route("/c/<conversation_id>/turns/<turn_id>/regenerate", methods=["POST"])
def regenerate_turn(conversation_id: str, turn_id: str):
    """Re-answer a turn under the current prompt. Admin-only (not in
    USER_ENDPOINTS) — regeneration exists to show a prompt edit paying off."""
    _require_schema()
    conv = _conversation_or_404(conversation_id)
    if not ids.valid("turn", turn_id):
        abort(404)
    try:
        turn = conversations.load_turn(turn_id)
    except FileNotFoundError:
        abort(404)
    if turn.conversation_id != conversation_id:
        abort(404)

    runs.enqueue_regenerate(
        conversation_id=conversation_id,
        turn_id=turn_id,
        prompt_id=_prompt_for_next_turn(),
        is_admin=(conv.role == "admin"),
    )
    flash("Re-answering that turn…", "success")
    return redirect(url_for("chat.conversation", conversation_id=conversation_id)
                    + f"#turn-{turn_id}")


@bp.route("/c/<conversation_id>/delete", methods=["POST"])
def delete_conversation(conversation_id: str):
    _require_schema()
    _conversation_or_404(conversation_id)
    conversations.delete(conversation_id)
    flash("Deleted conversation.", "success")
    return redirect(url_for("chat.conversations_list"))


# ---- Prompt revisions (admin) ---------------------------------------------

@bp.route("/c/<conversation_id>/revisions/<revision_id>/accept", methods=["POST"])
def accept_revision(conversation_id: str, revision_id: str):
    _require_schema()
    conv = _conversation_or_404(conversation_id)
    if not ids.valid("revision", revision_id):
        abort(404)
    try:
        result = revisions.accept(revision_id,
                                 is_admin_conversation=(conv.role == "admin"))
    except FileNotFoundError:
        abort(404)
    except (ValueError, FileExistsError) as exc:
        flash(str(exc), "error")
        return redirect(url_for("chat.conversation", conversation_id=conversation_id))
    flash(f"Saved {result['prompt'].prompt_id} and re-answering that turn…", "success")
    return redirect(url_for("chat.conversation", conversation_id=conversation_id))


@bp.route("/c/<conversation_id>/revisions/<revision_id>/dismiss", methods=["POST"])
def dismiss_revision(conversation_id: str, revision_id: str):
    _require_schema()
    _conversation_or_404(conversation_id)
    if not ids.valid("revision", revision_id):
        abort(404)
    try:
        revisions.dismiss(revision_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("chat.conversation", conversation_id=conversation_id))
    flash("Dismissed the proposal. Nothing was saved.", "success")
    return redirect(url_for("chat.conversation", conversation_id=conversation_id))


@bp.route("/c/<conversation_id>/revisions/<revision_id>/revert", methods=["POST"])
def revert_revision(conversation_id: str, revision_id: str):
    _require_schema()
    _conversation_or_404(conversation_id)
    if not ids.valid("revision", revision_id):
        abort(404)
    try:
        prompt = revisions.revert(revision_id)
    except FileNotFoundError:
        abort(404)
    except (ValueError, FileExistsError) as exc:
        flash(str(exc), "error")
        return redirect(url_for("chat.conversation", conversation_id=conversation_id))
    flash(f"Reverted: saved {prompt.prompt_id} with the earlier text.", "success")
    return redirect(url_for("chat.conversation", conversation_id=conversation_id))


# ---- Golden pairs (admin) -------------------------------------------------

@bp.route("/golden")
def golden_list():
    _require_schema()
    prompt_id = request.args.get("prompt_id", "").strip()
    if prompt_id and not dbio.valid_id("prompt", prompt_id):
        prompt_id = ""
    return render_template(
        "chat/golden.html",
        pairs=golden.list_pairs(prompt_id),
        prompt_ids=golden.prompt_ids_with_pairs(),
        selected_prompt_id=prompt_id,
    )


@bp.route("/golden/mark", methods=["POST"])
def mark_golden():
    """Toggle a response's golden-pair status."""
    _require_schema()
    turn_id = request.form.get("turn_id", "").strip()
    run_id = request.form.get("run_id", "").strip()
    conversation_id = request.form.get("conversation_id", "").strip()
    if not ids.valid("turn", turn_id) or not dbio.valid_id("run", run_id):
        abort(404)
    _conversation_or_404(conversation_id)

    if golden.for_run(run_id):
        golden.unmark(run_id)
        flash("Removed from golden pairs.", "success")
    else:
        try:
            golden.mark(turn_id, run_id, note=request.form.get("note", ""))
        except (FileNotFoundError, ValueError) as exc:
            flash(str(exc), "error")
            return redirect(url_for("chat.conversation", conversation_id=conversation_id))
        flash("Saved as a golden pair.", "success")
    return redirect(url_for("chat.conversation", conversation_id=conversation_id)
                    + f"#turn-{turn_id}")


@bp.route("/golden/<golden_id>/delete", methods=["POST"])
def delete_golden(golden_id: str):
    _require_schema()
    if not ids.valid("golden", golden_id):
        abort(404)
    try:
        golden.delete(golden_id)
    except FileNotFoundError:
        abort(404)
    flash("Deleted golden pair.", "success")
    return redirect(url_for("chat.golden_list"))
