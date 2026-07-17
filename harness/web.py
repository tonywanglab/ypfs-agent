"""Local supervisor UI for the two-variable evaluation harness."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

from . import config, dbio, reviews, tasks, versions
from .markdown_render import render_markdown
from .models import Case, RubricCriterion
from .rubric_diff import diff_rubric_criteria
from .rubric_markdown import criteria_to_markdown, markdown_to_criteria
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
    if task["status"] == "finished" and task["kind"] == tasks.KIND_RUBRIC_DRAFT:
        return url_for("view_rubric_draft", task_id=task["task_id"])
    return None


def _field_at(values: list[str], index: int) -> str:
    return values[index].strip() if index < len(values) else ""


def _review_is_used(review_id: str) -> bool:
    try:
        review = reviews.load_review(review_id)
    except (FileNotFoundError, ValueError):
        return False
    if review.status == "used":
        return True
    artifacts = [*versions.list_prompts(), *versions.list_rubrics()]
    return any(review_id in artifact.derived_from_review_ids for artifact in artifacts)


def create_app() -> Flask:
    app = Flask(__name__, template_folder=str(TEMPLATES), static_folder=str(STATIC))
    app.secret_key = "harness-local-dev-only"
    app.jinja_env.filters["markdown"] = render_markdown

    @app.context_processor
    def inject_globals():
        try:
            latest_prompt_id = versions.latest_prompt_id()
            latest_rubric_id = versions.latest_rubric_id()
        except FileNotFoundError:
            latest_prompt_id = latest_rubric_id = "not seeded"
        return {
            "latest_prompt_id": latest_prompt_id,
            "latest_rubric_id": latest_rubric_id,
            "fixed_agent_model": config.agent_model(),
            "fixed_judge_model": config.judge_model(),
            "fixed_agent_model_label": config.agent_model().rsplit("/", 1)[-1],
            "fixed_judge_model_label": config.judge_model().rsplit("/", 1)[-1],
        }

    @app.route("/")
    def dashboard():
        all_runs = list_runs()
        all_reviews = reviews.list_reviews()
        open_reviews = [review for review in all_reviews if review.status == "open"]
        reviewed_run_ids = {review.run_id for review in all_reviews}
        pending_runs = [run for run in all_runs if run.run_id not in reviewed_run_ids]
        pending_runs.sort(key=lambda run: run.created_at, reverse=True)
        return render_template(
            "dashboard.html",
            pending_runs=pending_runs,
            open_reviews=list(reversed(open_reviews)),
            prompts=versions.list_prompts(),
            rubrics=versions.list_rubrics(),
            prompt_reviews=versions.available_reviews("prompt_issue", open_reviews),
            rubric_reviews=versions.available_reviews("rubric_issue", open_reviews),
            prompt_draft_task_id=tasks.new_task_id(),
            rubric_draft_task_id=tasks.new_task_id(),
            active_tasks=tasks.list_active(),
        )

    @app.route("/runs")
    def runs_list():
        prompt_id = request.args.get("prompt_id", "").strip()
        rubric_id = request.args.get("rubric_id", "").strip()
        runs = list_runs()
        if prompt_id:
            runs = [run for run in runs if run.prompt_id == prompt_id]
        if rubric_id:
            runs = [run for run in runs if run.rubric_id == rubric_id]
        runs.sort(key=lambda run: run.created_at, reverse=True)
        return render_template(
            "runs.html",
            runs=runs,
            prompts=versions.list_prompts(),
            rubrics=versions.list_rubrics(),
            selected_prompt_id=prompt_id,
            selected_rubric_id=rubric_id,
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
        linked_reviews = reviews.reviews_for_run(run_id)
        if any(_review_is_used(review.review_id) for review in linked_reviews):
            flash("This run has reviews used by a saved version.", "error")
        else:
            for review in linked_reviews:
                reviews.delete_review(review.review_id)
            delete_run(run_id)
            flash(f"Deleted {run_id}.", "success")
        destination = "runs_list" if request.form.get("next") == "runs" else "dashboard"
        return redirect(url_for(destination))

    @app.route("/reviews/<review_id>/delete", methods=["POST"])
    def delete_review_route(review_id: str):
        if not dbio.valid_id("review", review_id):
            abort(404)
        try:
            review = reviews.load_review(review_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        if _review_is_used(review_id):
            flash("This review was used by a saved prompt or rubric version.", "error")
        else:
            try:
                reviews.delete_review(review_id)
            except ValueError as exc:
                flash(str(exc), "error")
            else:
                flash(f"Deleted review {review.review_id}.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/chat")
    def chat():
        prompts = versions.list_prompts()
        rubrics = versions.list_rubrics()
        return render_template(
            "chat.html",
            prompts=prompts,
            rubrics=rubrics,
            cases=[case.to_dict() for case in load_cases()],
            selected_prompt_id=request.args.get(
                "prompt_id",
                prompts[-1].prompt_id if prompts else "",
            ),
            selected_rubric_id=request.args.get(
                "rubric_id",
                rubrics[-1].rubric_id if rubrics else "",
            ),
            default_samples=1,
            openrouter_configured=_openrouter_configured(),
            task_id=tasks.new_task_id(),
        )

    @app.route("/chat/run", methods=["POST"])
    def chat_run():
        query = request.form.get("query", "").strip()
        prompt_id = request.form.get("prompt_id", "").strip()
        rubric_id = request.form.get("rubric_id", "").strip()
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
        if not prompt_id or not rubric_id:
            flash("Select a system prompt and judge rubric.", "error")
            return redirect(url_for("chat"))
        if not _openrouter_configured():
            flash("OPENROUTER_API_KEY is not set. Add it to .env and restart.", "error")
            return redirect(url_for("chat"))
        try:
            prompt = versions.load_prompt(prompt_id)
            rubric = versions.load_rubric(rubric_id)
        except (FileNotFoundError, ValueError):
            flash("Unknown prompt or rubric version.", "error")
            return redirect(url_for("chat"))

        case = Case(case_id=new_id("adhoc"), prompt=query, tags=["adhoc", "chat"])
        tasks.enqueue(
            tasks.KIND_EXPERIMENT,
            payload={
                "case": case.to_dict(),
                "prompt_id": prompt.prompt_id,
                "rubric_id": rubric.rubric_id,
                "agent_model": config.agent_model(),
                "judge_model": config.judge_model(),
                "samples": samples,
            },
            task_id=task_id,
        )
        label = f"{samples} sample{'s' if samples > 1 else ''}"
        flash(f"Queued run ({label}).", "success")
        return redirect(url_for("chat"))

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
        if task["status"] == "finished" and task["kind"] == tasks.KIND_RUBRIC_DRAFT:
            return redirect(url_for("view_rubric_draft", task_id=task_id))
        return render_template("task_detail.html", task=task)

    @app.route("/runs/<run_id>")
    def run_detail(run_id: str):
        if not dbio.valid_id("run", run_id):
            abort(404)
        try:
            bundle = load_run_bundle(run_id)
            rubric = versions.load_rubric(bundle["manifest"]["rubric_id"])
        except (FileNotFoundError, ValueError):
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
            "checks": sample["checks"],
            "judgment": sample["judgment"],
        }
        criteria_by_id = {criterion.id: criterion for criterion in rubric.criteria}
        return render_template(
            "run_detail.html",
            run_id=run_id,
            bundle=display,
            sample_count=len(bundle["samples"]),
            selected_sample=sample["index"],
            criteria_by_id=criteria_by_id,
            existing_reviews=reviews.reviews_for_run(run_id),
            trace_events=trace_timeline(display.get("trace")),
        )

    @app.route("/runs/<run_id>/review", methods=["POST"])
    def submit_review(run_id: str):
        if not dbio.valid_id("run", run_id):
            abort(404)
        try:
            load_manifest(run_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        verdicts = request.form.getlist("verdict")
        if not verdicts:
            flash("Add at least one review.", "error")
            return redirect(url_for("run_detail", run_id=run_id))
        problems = request.form.getlist("primary_problem")
        targets = request.form.getlist("failure_attribution")
        missing_lists = request.form.getlist("missing_considerations")
        notes = request.form.getlist("notes")
        valid_targets = {"prompt_issue", "rubric_issue", "invalid_run"}
        for index, verdict in enumerate(verdicts):
            if verdict not in ("acceptable", "unacceptable"):
                flash("Invalid verdict.", "error")
                return redirect(url_for("run_detail", run_id=run_id))
            target = _field_at(targets, index) or None
            if verdict == "unacceptable" and target not in valid_targets:
                flash("Choose what should change for an unacceptable run.", "error")
                return redirect(url_for("run_detail", run_id=run_id))
            if verdict == "acceptable":
                target = None
            reviews.create_review(
                run_id=run_id,
                verdict=verdict,
                primary_problem=_field_at(problems, index),
                failure_attribution=target,
                missing_considerations=[
                    line.strip()
                    for line in _field_at(missing_lists, index).splitlines()
                    if line.strip()
                ],
                notes=_field_at(notes, index),
            )
        flash(f"Saved {len(verdicts)} review(s).", "success")
        return redirect(url_for("run_detail", run_id=run_id))

    @app.route("/versions/prompts/draft", methods=["POST"])
    def draft_prompt():
        base_id = request.form.get("base_id", "").strip()
        review_ids = request.form.getlist("review_ids")
        task_id = request.form.get("task_id", "").strip()
        if not tasks.is_task_id(task_id):
            task_id = tasks.new_task_id()
        tasks.enqueue(
            tasks.KIND_PROMPT_DRAFT,
            payload={"base_id": base_id, "review_ids": review_ids},
            task_id=task_id,
        )
        flash("Generating prompt draft…", "success")
        return redirect(url_for("dashboard"))

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
        try:
            base = versions.load_prompt(draft.get("base_id"))
        except (FileNotFoundError, ValueError):
            abort(404)
        return render_template(
            "prompt_draft.html",
            draft=draft,
            diff_groups=build_line_diff(base.text, draft.get("prompt_text", "")),
        )

    @app.route("/versions/prompts/save", methods=["POST"])
    def save_prompt():
        try:
            prompt = versions.save_prompt(
                base_prompt_id=request.form.get("base_id", "").strip(),
                text=request.form.get("prompt_text", ""),
                rationale=request.form.get("rationale", ""),
                review_ids=request.form.getlist("review_ids"),
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
                review_ids=[],
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

    @app.route("/versions/rubrics/draft", methods=["POST"])
    def draft_rubric():
        base_id = request.form.get("base_id", "").strip()
        review_ids = request.form.getlist("review_ids")
        task_id = request.form.get("task_id", "").strip()
        if not tasks.is_task_id(task_id):
            task_id = tasks.new_task_id()
        tasks.enqueue(
            tasks.KIND_RUBRIC_DRAFT,
            payload={"base_id": base_id, "review_ids": review_ids},
            task_id=task_id,
        )
        flash("Generating rubric draft…", "success")
        return redirect(url_for("dashboard"))

    @app.route("/versions/rubrics/draft/<task_id>")
    def view_rubric_draft(task_id: str):
        if not tasks.is_task_id(task_id):
            abort(404)
        try:
            task = tasks.load(task_id)
        except FileNotFoundError:
            abort(404)
        if task["kind"] != tasks.KIND_RUBRIC_DRAFT or task["status"] != "finished":
            abort(404)
        draft = task["result"] or {}
        try:
            base = versions.load_rubric(draft.get("base_id"))
            proposed = [RubricCriterion.from_dict(item) for item in draft.get("criteria", [])]
        except (FileNotFoundError, ValueError):
            abort(404)
        return render_template(
            "rubric_draft.html",
            draft=draft,
            criteria_json=json.dumps(draft.get("criteria", []), indent=2),
            diff_rows=diff_rubric_criteria(base.criteria, proposed),
        )

    @app.route("/versions/rubrics/save", methods=["POST"])
    def save_rubric():
        criteria_json = request.form.get("criteria_json", "")
        try:
            raw = json.loads(criteria_json)
            if not isinstance(raw, list):
                raise ValueError("Criteria JSON must be a list")
            criteria = [RubricCriterion.from_dict(item) for item in raw]
            rubric = versions.save_rubric(
                base_rubric_id=request.form.get("base_id", "").strip(),
                criteria=criteria,
                rationale=request.form.get("rationale", ""),
                review_ids=request.form.getlist("review_ids"),
            )
        except (json.JSONDecodeError, FileNotFoundError, FileExistsError, ValueError) as exc:
            flash(str(exc), "error")
            return redirect(url_for("dashboard"))
        flash(f"Saved immutable version {rubric.rubric_id}.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/versions/rubrics/<rubric_id>")
    def edit_rubric_version(rubric_id: str):
        if not dbio.valid_id("rubric", rubric_id):
            abort(404)
        try:
            rubric = versions.load_rubric(rubric_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        return render_template(
            "rubric_edit.html",
            rubric=rubric,
            criteria_markdown=criteria_to_markdown(rubric.criteria),
            rationale="",
        )

    @app.route("/versions/rubrics/<rubric_id>/save", methods=["POST"])
    def save_rubric_version(rubric_id: str):
        if not dbio.valid_id("rubric", rubric_id):
            abort(404)
        criteria_markdown = request.form.get("criteria_markdown", "")
        rationale = request.form.get("rationale", "")
        try:
            versions.load_rubric(rubric_id)
            criteria = markdown_to_criteria(criteria_markdown)
            versions.validate_criteria(criteria)
            rubric = versions.save_rubric(
                base_rubric_id=rubric_id,
                criteria=criteria,
                rationale=rationale or f"Manual edit of {rubric_id}",
                review_ids=[],
            )
        except (FileNotFoundError, FileExistsError, ValueError) as exc:
            try:
                rubric = versions.load_rubric(rubric_id)
            except (FileNotFoundError, ValueError):
                abort(404)
            flash(str(exc), "error")
            return render_template(
                "rubric_edit.html",
                rubric=rubric,
                criteria_markdown=criteria_markdown,
                rationale=rationale,
            ), 400
        flash(f"Saved immutable version {rubric.rubric_id}.", "success")
        return redirect(url_for("dashboard"))

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
