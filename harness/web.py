"""Local supervisor UI for the evaluation harness."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

from . import config, dbio, feedback, tasks, versions
from .chat import auth as chat_auth
from .chat import web as chat_web
from .markdown_render import render_markdown
from .models import Case
from .runner import delete_run, load_manifest, load_run_bundle, list_runs
from .seed import load_cases
from .storage import new_id
from .text_diff import build_line_diff
from .trace import trace_timeline

load_dotenv()

TEMPLATES = Path(__file__).parent / "templates"
STATIC = Path(__file__).parent / "static"


def _openrouter_configured() -> bool:
    return bool(os.environ.get("OPENROUTER_API_KEY"))


def _task_result_url(task: dict) -> str | None:
    """Where a task's outcome can be viewed, or None while there's nothing to show yet."""
    if task["run_id"]:
        return url_for("run_detail", run_id=task["run_id"])
    if task["status"] == "finished" and task["kind"] == tasks.KIND_PROMPT_DRAFT:
        return url_for("view_prompt_draft", task_id=task["task_id"])
    return None


def _run_label(query: str, word_limit: int = 8) -> str:
    words = query.split()
    snippet = " ".join(words[:word_limit])
    return snippet + "…" if len(words) > word_limit else snippet


def create_app() -> Flask:
    app = Flask(__name__, template_folder=str(TEMPLATES), static_folder=str(STATIC))
    # The session now carries an authorization decision (the admin role), so a
    # hardcoded key won't do. An absent HARNESS_SECRET_KEY gets a per-process
    # random one: sessions don't survive a restart, which is fine locally.
    app.secret_key = os.environ.get("HARNESS_SECRET_KEY") or secrets.token_hex(32)
    # Local supervisor UI: always pick up template edits without --debug.
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.jinja_env.filters["markdown"] = render_markdown

    app.register_blueprint(chat_web.bp)
    chat_auth.install_guards(app)

    @app.context_processor
    def inject_globals():
        # This runs on EVERY render, including /login. A database hiccup here
        # would 500 whatever page the operator was looking at, so it degrades to
        # a placeholder chip instead of taking the page down.
        try:
            latest_prompt_id = versions.latest_prompt_id()
        except FileNotFoundError:
            latest_prompt_id = "not seeded"
        except Exception:
            latest_prompt_id = "unavailable"
        return {
            "latest_prompt_id": latest_prompt_id,
            "fixed_agent_model": config.agent_model(),
            "fixed_agent_model_label": config.agent_model().rsplit("/", 1)[-1],
            "is_admin": chat_auth.is_admin(),
            "current_role": chat_auth.current_role(),
            "admin_enabled": chat_auth.admin_enabled(),
        }

    @app.route("/")
    def dashboard():
        all_runs = list_runs()
        recent_runs = sorted(
            (run for run in all_runs if run.status == "complete"),
            key=lambda run: run.created_at,
            reverse=True,
        )
        snapshots = dbio.q(
            "SELECT run_id, case_snapshot->>'prompt' AS query FROM runs WHERE run_id = ANY(%s)",
            ([run.run_id for run in recent_runs],),
        ) if recent_runs else []
        run_labels = {
            row["run_id"]: _run_label(row["query"] or "") for row in snapshots
        }
        active_tasks = sorted(
            tasks.list_active(),
            key=lambda task: task["created_at"] or "",
        )
        return render_template(
            "dashboard.html",
            recent_runs=recent_runs,
            run_labels=run_labels,
            prompts=versions.list_prompts(),
            active_tasks=active_tasks,
        )

    @app.route("/runs")
    def runs_list():
        prompt_id = request.args.get("prompt_id", "").strip()
        runs = list_runs()
        if prompt_id:
            runs = [run for run in runs if run.prompt_id == prompt_id]
        runs.sort(key=lambda run: run.created_at, reverse=True)
        return render_template(
            "runs.html",
            runs=runs,
            prompts=versions.list_prompts(),
            selected_prompt_id=prompt_id,
        )

    @app.route("/runs/<run_id>/delete", methods=["POST"])
    def delete_run_route(run_id: str):
        if request.form.get("next") != "runs":
            flash("Delete runs from the Runs page.", "error")
            return redirect(url_for("dashboard"))
        if not dbio.valid_id("run", run_id):
            abort(404)
        try:
            load_manifest(run_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        delete_run(run_id)
        flash(f"Deleted {run_id}.", "success")
        destination = "runs_list" if request.form.get("next") == "runs" else "dashboard"
        return redirect(url_for(destination))

    @app.route("/chat")
    def chat():
        prompts = versions.list_prompts()
        queued_runs = [
            task for task in tasks.list_active() if task["kind"] == tasks.KIND_EXPERIMENT
        ]
        queued_runs.sort(key=lambda task: task["created_at"] or "")
        return render_template(
            "chat.html",
            prompts=prompts,
            cases=[case.to_dict() for case in load_cases()],
            selected_prompt_id=request.args.get(
                "prompt_id",
                prompts[-1].prompt_id if prompts else "",
            ),
            default_samples=1,
            openrouter_configured=_openrouter_configured(),
            task_id=tasks.new_task_id(),
            queued_runs=queued_runs,
        )

    @app.route("/chat/run", methods=["POST"])
    def chat_run():
        query = request.form.get("query", "").strip()
        prompt_id = request.form.get("prompt_id", "").strip()
        task_id = request.form.get("task_id", "").strip()
        try:
            samples = max(1, min(int(request.form.get("samples", "1")), 20))
        except ValueError:
            samples = 1
        if not query:
            flash("Enter a query to run.", "error")
            return redirect(url_for("chat"))
        if not tasks.is_task_id(task_id):
            flash("Invalid task ID. Reload the page and try again.", "error")
            return redirect(url_for("chat"))
        if not prompt_id:
            flash("Select a system prompt.", "error")
            return redirect(url_for("chat"))
        if not _openrouter_configured():
            flash("OPENROUTER_API_KEY is not set. Add it to .env and restart.", "error")
            return redirect(url_for("chat"))
        try:
            prompt = versions.load_prompt(prompt_id)
        except (FileNotFoundError, ValueError):
            flash("Unknown prompt version.", "error")
            return redirect(url_for("chat"))

        case = Case(case_id=new_id("adhoc"), prompt=query, tags=["adhoc", "chat"])
        tasks.enqueue(
            tasks.KIND_EXPERIMENT,
            payload={
                "case": case.to_dict(),
                "prompt_id": prompt.prompt_id,
                "agent_model": config.agent_model(),
                "samples": samples,
            },
            task_id=task_id,
        )
        label = f"{samples} sample{'s' if samples > 1 else ''}"
        flash(f"Queued run ({label}).", "success")
        return redirect(url_for("chat"))

    @app.route("/tasks/active")
    def tasks_active():
        kind = request.args.get("kind", "all").strip()
        active = tasks.list_active()
        if kind and kind != "all":
            active = [task for task in active if task["kind"] == kind]
        return jsonify(active)

    @app.route("/tasks/<task_id>/status")
    def task_status(task_id: str):
        if not dbio.valid_id("task", task_id):
            abort(404)
        try:
            task = tasks.load(task_id)
        except FileNotFoundError:
            return jsonify({"status": "queued"}), 404
        return jsonify({**task, "result_url": _task_result_url(task)})

    @app.route("/tasks/<task_id>")
    def task_detail(task_id: str):
        if not dbio.valid_id("task", task_id):
            abort(404)
        try:
            task = tasks.load(task_id)
        except FileNotFoundError:
            abort(404)
        if task["run_id"]:
            return redirect(url_for("run_detail", run_id=task["run_id"]))
        if task["status"] == "finished" and task["kind"] == tasks.KIND_PROMPT_DRAFT:
            return redirect(url_for("view_prompt_draft", task_id=task_id))
        return render_template("task_detail.html", task=task)

    @app.route("/runs/<run_id>")
    def run_detail(run_id: str):
        if not dbio.valid_id("run", run_id):
            abort(404)
        try:
            bundle = load_run_bundle(run_id)
        except FileNotFoundError:
            abort(404)
        selected_sample = request.args.get("sample")
        if selected_sample is not None:
            try:
                selected_index = int(selected_sample)
            except ValueError:
                selected_index = bundle["samples"][0]["index"]
        else:
            selected_index = bundle["samples"][0]["index"]
        sample = next(
            (item for item in bundle["samples"] if item["index"] == selected_index),
            bundle["samples"][0],
        )
        display = {
            **bundle,
            "answer": sample["answer"],
            "trace": sample["trace"],
        }
        return render_template(
            "run_detail.html",
            run_id=run_id,
            bundle=display,
            sample_count=len(bundle["samples"]),
            selected_sample=sample["index"],
            feedback_items=feedback.feedback_for_run(run_id),
            draft_task_id=tasks.new_task_id(),
            trace_events=trace_timeline(display.get("trace")),
        )

    @app.route("/runs/<run_id>/feedback", methods=["POST"])
    def create_feedback(run_id: str):
        if not dbio.valid_id("run", run_id):
            abort(404)
        try:
            load_manifest(run_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        payload = request.get_json(silent=True) or {}
        try:
            sample_index = int(payload.get("sample_index"))
        except (TypeError, ValueError):
            return jsonify({"error": "sample_index must be an integer"}), 400
        selected_text = payload.get("selected_text", "")
        comment = payload.get("comment", "")
        if not isinstance(selected_text, str) or not isinstance(comment, str):
            return jsonify({"error": "selected_text and comment must be strings"}), 400
        sample_exists = dbio.q1(
            "SELECT 1 FROM run_samples WHERE run_id = %s AND sample_index = %s",
            (run_id, sample_index),
        )
        if sample_exists is None:
            return jsonify({"error": "Unknown sample for this run"}), 400
        try:
            item = feedback.create_feedback(run_id, sample_index, selected_text, comment)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"feedback": item.to_dict()}), 201

    @app.route("/feedback/<feedback_id>/delete", methods=["POST"])
    def delete_feedback_route(feedback_id: str):
        if not dbio.valid_id("feedback", feedback_id):
            abort(404)
        try:
            item = feedback.delete_feedback(feedback_id)
        except FileNotFoundError:
            abort(404)
        wants_json = (
            request.headers.get("X-Requested-With") == "XMLHttpRequest"
            or request.accept_mimetypes.best_match(["application/json", "text/html"])
            == "application/json"
        )
        if wants_json:
            return jsonify({"ok": True, "feedback_id": item.feedback_id, "run_id": item.run_id})
        flash("Deleted feedback.", "success")
        return redirect(url_for("run_detail", run_id=item.run_id) + "#feedback")

    @app.route("/runs/<run_id>/feedback/draft", methods=["POST"])
    def draft_prompt_from_feedback(run_id: str):
        if not dbio.valid_id("run", run_id):
            abort(404)
        try:
            manifest = load_manifest(run_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        items = feedback.feedback_for_run(run_id)
        if not items:
            flash("Add at least one feedback item before proposing edits.", "error")
            return redirect(url_for("run_detail", run_id=run_id))
        task_id = request.form.get("task_id", "").strip()
        if not tasks.is_task_id(task_id):
            task_id = tasks.new_task_id()
        tasks.enqueue(
            tasks.KIND_PROMPT_DRAFT,
            payload={
                "base_id": versions.latest_prompt_id(),
                "feedback_ids": [item.feedback_id for item in items],
            },
            task_id=task_id,
        )
        flash("Generating prompt draft…", "success")
        return redirect(url_for("run_detail", run_id=run_id))

    @app.route("/versions/prompts/draft/<task_id>")
    def view_prompt_draft(task_id: str):
        if not tasks.is_task_id(task_id):
            abort(404)
        try:
            task = tasks.load(task_id)
        except FileNotFoundError:
            abort(404)
        if task["kind"] != tasks.KIND_PROMPT_DRAFT or task["status"] != "finished":
            abort(404)
        draft = task["result"] or {}
        current = versions.latest_prompt()
        draft_text = draft.get("prompt_text", "")
        return render_template(
            "prompt_draft.html",
            draft=draft,
            current_prompt=current,
            diff_groups=build_line_diff(current.text, draft_text),
        )

    @app.route("/versions/prompts/diff", methods=["POST"])
    def prompt_diff():
        data = request.get_json(silent=True) or {}
        before = data.get("before", "")
        after = data.get("after", "")
        current_id = (data.get("current_id") or "current").strip() or "current"
        return render_template(
            "partials/prompt_diff.html",
            diff_groups=build_line_diff(before, after),
            current_id=current_id,
        )

    @app.route("/versions/prompts/save", methods=["POST"])
    def save_prompt():
        try:
            prompt = versions.save_prompt(
                base_prompt_id=request.form.get("base_id", "").strip(),
                text=request.form.get("prompt_text", ""),
                rationale=request.form.get("rationale", ""),
            )
        except (FileNotFoundError, FileExistsError, ValueError) as exc:
            flash(str(exc), "error")
            return redirect(url_for("dashboard"))
        flash(f"Saved immutable version {prompt.prompt_id}.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/versions/prompts/<prompt_id>")
    def edit_prompt_version(prompt_id: str):
        if not dbio.valid_id("prompt", prompt_id):
            abort(404)
        try:
            prompt = versions.load_prompt(prompt_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        return render_template(
            "prompt_edit.html",
            prompt=prompt,
            prompt_text=prompt.text,
            rationale="",
        )

    @app.route("/versions/prompts/<prompt_id>/save", methods=["POST"])
    def save_prompt_version(prompt_id: str):
        if not dbio.valid_id("prompt", prompt_id):
            abort(404)
        prompt_text = request.form.get("prompt_text", "")
        rationale = request.form.get("rationale", "")
        try:
            versions.load_prompt(prompt_id)
            prompt = versions.save_prompt(
                base_prompt_id=prompt_id,
                text=prompt_text,
                rationale=rationale or f"Manual edit of {prompt_id}",
            )
        except (FileNotFoundError, FileExistsError, ValueError) as exc:
            try:
                prompt = versions.load_prompt(prompt_id)
            except (FileNotFoundError, ValueError):
                abort(404)
            flash(str(exc), "error")
            return render_template(
                "prompt_edit.html",
                prompt=prompt,
                prompt_text=prompt_text,
                rationale=rationale,
            ), 400
        flash(f"Saved immutable version {prompt.prompt_id}.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/markdown/preview", methods=["POST"])
    def markdown_preview():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")
        if not isinstance(text, str):
            return jsonify({"error": "text must be a string"}), 400
        return jsonify({"html": render_markdown(text)})

    return app


def main(host: str = "127.0.0.1", port: int = 5050, debug: bool = False) -> None:
    app = create_app()
    print(f"Supervisor UI: http://{host}:{port}/")
    # Flask's dev server defaults threaded=True, which spawns a fresh OS
    # thread per request — that starves db.get_thread_conn()'s per-thread
    # connection cache (never reused, since the thread that opened it is
    # gone by the next request) and pays a full Postgres reconnect on every
    # single page load. Single-threaded keeps the cache doing its job; the
    # local supervisor UI has one operator, so there's no concurrency to gain.
    app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=False)
