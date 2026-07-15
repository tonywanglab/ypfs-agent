"""Local supervisor web UI for the two-loop evaluation harness.

Bind to 127.0.0.1 only — no authentication in v1. All reads go through
safe_path(); POST handlers never accept arbitrary filesystem paths.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for

from agent.agent import DEFAULT_MODEL

from . import candidates, registry, reviews, router
from .agent_models import AGENT_MODEL_OPTIONS, default_model_slug, is_valid_model_slug
from .candidates import (
    load_prompt,
    load_prompt_candidate,
    load_prompt_version,
    load_proposal,
    load_rubric,
    load_rubric_version,
    require_current_prompt_candidate,
)
from .models import Case
from .promote import deny_promotion, promote_prompt
from .runner import (
    load_pairs,
    load_promotion,
    load_run_bundle,
    list_promotions,
    list_runs,
    run_ab,
    run_case,
    set_pair_preference,
)
from .seed import load_cases
from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json, safe_path

LAUNCHES_DIR = EVALS_DIR / "launches"

load_dotenv()

TEMPLATES = Path(__file__).parent / "templates"
STATIC = Path(__file__).parent / "static"


def _openrouter_configured() -> bool:
    return bool(os.environ.get("OPENROUTER_API_KEY"))


def _run_launch_error_message(exc: BaseException) -> str:
    if isinstance(exc, KeyError) and exc.args and exc.args[0] == "OPENROUTER_API_KEY":
        return "OPENROUTER_API_KEY is not set. Add it to .env at the repo root and restart the server."
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return f"OpenRouter request failed ({exc.response.status_code}): {exc.response.text[:200]}"
    return f"Run failed: {exc}"


def create_app() -> Flask:
    app = Flask(__name__, template_folder=str(TEMPLATES), static_folder=str(STATIC))
    app.secret_key = "harness-local-dev-only"

    @app.context_processor
    def inject_globals():
        return {
            "locked_branch": registry.locked_branch(),
            "pending_queue": registry.pending_queue(),
            "active_rubric_id": registry.active_rubric_id(),
            "active_prompt_id": registry.active_prompt_id(),
        }

    @app.route("/")
    def dashboard():
        all_runs = list_runs()
        reviewed_run_ids = {r.run_id for r in reviews.list_reviews()}
        pending_runs = [m for m in all_runs if m.run_id not in reviewed_run_ids]
        return render_template(
            "dashboard.html",
            pending_runs=pending_runs,
            proposals=candidates.list_proposals(),
            prompt_candidates=candidates.list_prompt_candidates(),
            promotions=list_promotions(),
            reviews=reviews.list_reviews(),
        )

    @app.route("/runs")
    def runs_list():
        return render_template("runs.html", runs=list_runs())

    @app.route("/chat")
    def chat():
        return render_template(
            "chat.html",
            prompts=candidates.list_selectable_prompts(),
            rubrics=candidates.list_selectable_rubrics(),
            cases=[c.to_dict() for c in load_cases()],
            models=AGENT_MODEL_OPTIONS,
            selected_model=default_model_slug(),
            selected_prompt_id=request.args.get("prompt_id", registry.active_prompt_id()),
            selected_rubric_id=request.args.get("rubric_id", registry.active_rubric_id()),
            default_samples=1,
            openrouter_configured=_openrouter_configured(),
        )

    @app.route("/chat/run", methods=["POST"])
    def chat_run():
        query = request.form.get("query", "").strip()
        prompt_id = request.form.get("prompt_id", "").strip()
        rubric_id = request.form.get("rubric_id", "").strip()
        model = request.form.get("model", default_model_slug()).strip()
        try:
            samples = max(1, min(int(request.form.get("samples", "1")), 20))
        except ValueError:
            samples = 1

        if not query:
            flash("Enter a query to run.", "error")
            return redirect(url_for("chat"))
        if not prompt_id or not rubric_id:
            flash("Select a system prompt and rubric.", "error")
            return redirect(url_for("chat"))
        if not is_valid_model_slug(model):
            flash("Select a valid model.", "error")
            return redirect(url_for("chat"))
        if not _openrouter_configured():
            flash(
                "OPENROUTER_API_KEY is not set. Add it to .env at the repo root and restart the server.",
                "error",
            )
            return redirect(url_for("chat"))

        try:
            prompt = load_prompt_version(prompt_id)
        except (FileNotFoundError, ValueError):
            flash(f"Unknown prompt {prompt_id!r}.", "error")
            return redirect(url_for("chat"))

        try:
            rubric = load_rubric_version(rubric_id)
        except (FileNotFoundError, ValueError):
            flash(f"Unknown rubric {rubric_id!r}.", "error")
            return redirect(url_for("chat"))

        launch_id = new_id("launch")
        run_ids: list[str] = []
        base_case_id = new_id("adhoc")
        try:
            for sample_index in range(samples):
                case = Case(
                    case_id=f"{base_case_id}_s{sample_index + 1}" if samples > 1 else base_case_id,
                    prompt=query,
                    tags=["adhoc", "chat"],
                )
                manifest = run_case(case, prompt.text, prompt.prompt_id, model, rubric, role="adhoc")
                run_ids.append(manifest.run_id)
        except (KeyError, requests.RequestException, RuntimeError, ValueError) as exc:
            flash(_run_launch_error_message(exc), "error")
            if run_ids:
                flash(
                    f"Partial batch: {len(run_ids)} of {samples} sample(s) completed before the failure.",
                    "warning",
                )
            return redirect(url_for("chat"))

        LAUNCHES_DIR.mkdir(parents=True, exist_ok=True)
        atomic_write_json(LAUNCHES_DIR / f"{launch_id}.json", {
            "launch_id": launch_id,
            "query": query,
            "prompt_id": prompt.prompt_id,
            "rubric_id": rubric.rubric_id,
            "model": model,
            "samples": samples,
            "run_ids": run_ids,
            "created_at": now_iso(),
        })

        if samples == 1:
            flash("Run complete.", "success")
            return redirect(url_for("run_detail", run_id=run_ids[0]))
        flash(f"Started {samples} sample runs.", "success")
        return redirect(url_for("launch_detail", launch_id=launch_id))

    @app.route("/chat/launches/<launch_id>")
    def launch_detail(launch_id: str):
        safe_path("launches", f"{launch_id}.json")
        try:
            launch = read_json(LAUNCHES_DIR / f"{launch_id}.json")
        except FileNotFoundError:
            abort(404)
        runs = []
        for run_id in launch.get("run_ids", []):
            safe_path("runs", run_id)
            try:
                bundle = load_run_bundle(run_id)
                runs.append({
                    "run_id": run_id,
                    "manifest": bundle["manifest"],
                    "answer": bundle["answer"],
                    "judgment": bundle["judgment"],
                })
            except (FileNotFoundError, ValueError):
                runs.append({"run_id": run_id, "manifest": {}, "answer": "", "judgment": {}})
        return render_template("launch_detail.html", launch=launch, runs=runs)

    @app.route("/runs/<run_id>")
    def run_detail(run_id: str):
        safe_path("runs", run_id)
        try:
            bundle = load_run_bundle(run_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        existing = reviews.reviews_for_run(run_id)
        return render_template(
            "run_detail.html",
            run_id=run_id,
            bundle=bundle,
            existing_reviews=existing,
        )

    @app.route("/runs/<run_id>/review", methods=["POST"])
    def submit_review(run_id: str):
        safe_path("runs", run_id)
        verdict = request.form.get("verdict", "")
        if verdict not in ("acceptable", "unacceptable"):
            flash("Invalid verdict.", "error")
            return redirect(url_for("run_detail", run_id=run_id))

        review = reviews.create_review(
            run_id=run_id,
            verdict=verdict,
            primary_problem=request.form.get("primary_problem", "").strip(),
            failure_attribution=request.form.get("failure_attribution", "ambiguous"),
            missing_considerations=[
                s.strip() for s in request.form.get("missing_considerations", "").split("\n") if s.strip()
            ],
            notes=request.form.get("notes", "").strip(),
        )
        status = router.route_review(review)
        if status["queued"]:
            flash(
                f"Review saved. The {status['branch']} branch is locked — "
                f"queued for the next cycle.",
                "warning",
            )
        elif status["action"] == "ready":
            flash(f"Review saved. Ready to start {status['branch']} update.", "success")
        else:
            flash("Review saved.", "success")
        return redirect(url_for("run_detail", run_id=run_id))

    @app.route("/proposals/rubric", methods=["POST"])
    def create_rubric_proposal():
        review_ids = request.form.getlist("review_ids")
        model = request.form.get("model", "anthropic/claude-sonnet-4-6")
        try:
            proposal = candidates.propose_rubric(review_ids, model)
        except registry.CycleLockedError as exc:
            for rid in review_ids:
                registry.enqueue("rubric", rid)
            flash(str(exc), "warning")
            return redirect(url_for("dashboard"))
        flash(f"Rubric proposal {proposal.rubric_id} created.", "success")
        return redirect(url_for("rubric_proposal", proposal_id=proposal.rubric_id))

    @app.route("/proposals/prompt", methods=["POST"])
    def create_prompt_proposal():
        review_ids = request.form.getlist("review_ids")
        model = request.form.get("model", "anthropic/claude-sonnet-4-6")
        try:
            candidate = candidates.propose_prompt(review_ids, model)
        except registry.CycleLockedError as exc:
            for rid in review_ids:
                registry.enqueue("prompt", rid)
            flash(str(exc), "warning")
            return redirect(url_for("dashboard"))
        flash(f"Prompt candidate {candidate.prompt_id} created.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/rubrics/proposals/<proposal_id>")
    def rubric_proposal(proposal_id: str):
        safe_path("rubrics", "proposals", f"{proposal_id}.json")
        try:
            proposal = load_proposal(proposal_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        parent = None
        if proposal.parent_rubric_id:
            try:
                parent = load_rubric(proposal.parent_rubric_id)
            except (FileNotFoundError, ValueError):
                parent = None
        return render_template(
            "rubric_proposal.html",
            proposal=proposal,
            parent=parent,
            criteria_json=json.dumps([c.to_dict() for c in proposal.criteria], indent=2),
        )

    @app.route("/rubrics/proposals/<proposal_id>/approve", methods=["POST"])
    def approve_rubric_proposal(proposal_id: str):
        safe_path("rubrics", "proposals", f"{proposal_id}.json")
        submitted_criteria = request.form.get("criteria_json", "")
        criteria_json = submitted_criteria.strip() or None
        try:
            frozen = candidates.approve_rubric(proposal_id, criteria_json=criteria_json)
        except ValueError as exc:
            flash(str(exc), "error")
            proposal = load_proposal(proposal_id)
            parent = None
            if proposal.parent_rubric_id:
                try:
                    parent = load_rubric(proposal.parent_rubric_id)
                except (FileNotFoundError, ValueError):
                    pass
            return render_template(
                "rubric_proposal.html",
                proposal=proposal,
                parent=parent,
                criteria_json=submitted_criteria,
            ), 400
        flash(f"Approved {frozen.rubric_id} as active rubric.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/rubrics/proposals/<proposal_id>/deny", methods=["POST"])
    def deny_rubric_proposal(proposal_id: str):
        safe_path("rubrics", "proposals", f"{proposal_id}.json")
        candidates.deny_rubric(proposal_id)
        flash(f"Denied rubric proposal {proposal_id}.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/prompts/candidates/<prompt_id>")
    def prompt_candidate(prompt_id: str):
        safe_path("prompts", "candidates", f"{prompt_id}.json")
        try:
            candidate = load_prompt_candidate(prompt_id)
        except (FileNotFoundError, ValueError):
            abort(404)
        return render_template(
            "prompt_candidate.html",
            candidate=candidate,
            prompt_text=candidate.text,
        )

    @app.route("/prompts/candidates/<prompt_id>/save", methods=["POST"])
    def save_prompt_candidate(prompt_id: str):
        safe_path("prompts", "candidates", f"{prompt_id}.json")
        submitted_text = request.form.get("text", "")
        try:
            candidate = candidates.update_prompt_candidate(prompt_id, submitted_text)
        except (FileNotFoundError, ValueError) as exc:
            try:
                candidate = load_prompt_candidate(prompt_id)
            except (FileNotFoundError, ValueError):
                abort(404)
            flash(str(exc), "error")
            return render_template(
                "prompt_candidate.html",
                candidate=candidate,
                prompt_text=submitted_text,
            ), 400
        flash(f"Saved prompt candidate {prompt_id}.", "success")
        return redirect(url_for("prompt_candidate", prompt_id=prompt_id))

    @app.route("/prompts/candidates/<prompt_id>/deny", methods=["POST"])
    def deny_prompt_candidate(prompt_id: str):
        safe_path("prompts", "candidates", f"{prompt_id}.json")
        candidates.deny_prompt(prompt_id)
        flash(f"Denied prompt candidate {prompt_id}.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/promotions/create", methods=["POST"])
    def create_promotion():
        candidate_id = request.form.get("candidate_prompt_id", "")
        case_ids = request.form.getlist("case_ids")
        model = request.form.get("model", "anthropic/claude-sonnet-4-6")
        if not candidate_id:
            flash("Select a prompt candidate.", "error")
            return redirect(url_for("dashboard"))

        all_cases = {c.case_id: c for c in load_cases()}
        selected = [all_cases[cid] for cid in case_ids if cid in all_cases]
        if not selected:
            flash("Select at least one case.", "error")
            return redirect(url_for("dashboard"))

        rubric = load_rubric(registry.active_rubric_id())
        incumbent = load_prompt(registry.active_prompt_id())
        try:
            candidate = require_current_prompt_candidate(candidate_id)
        except (FileNotFoundError, ValueError) as exc:
            flash(str(exc), "error")
            return redirect(url_for("dashboard"))

        promotion = run_ab(
            selected,
            rubric,
            incumbent.text,
            incumbent.prompt_id,
            candidate.text,
            candidate.prompt_id,
            model,
            cycle_id=candidate.cycle_id,
        )
        flash(f"A/B promotion {promotion.promotion_id} started.", "success")
        return redirect(url_for("promotion_detail", promotion_id=promotion.promotion_id))

    @app.route("/promotions/<promotion_id>")
    def promotion_detail(promotion_id: str):
        safe_path("promotions", promotion_id)
        try:
            promotion = load_promotion(promotion_id)
            pairs = load_pairs(promotion_id)
        except (FileNotFoundError, ValueError):
            abort(404)

        rubric = load_rubric(promotion.rubric_id)
        pair_views = []
        for pair in pairs:
            swap = _blind_swap(promotion_id, pair.case_id)
            inc_bundle = load_run_bundle(pair.incumbent_run_id)
            cand_bundle = load_run_bundle(pair.candidate_run_id)
            if swap:
                first, second = cand_bundle, inc_bundle
                first_label, second_label = "A", "B"
            else:
                first, second = inc_bundle, cand_bundle
                first_label, second_label = "A", "B"
            pair_views.append({
                "pair": pair,
                "case_id": pair.case_id,
                "first": first,
                "second": second,
                "first_label": first_label,
                "second_label": second_label,
                "swap": swap,
            })

        blocked = any(
            load_run_bundle(p.candidate_run_id)["manifest"].get("promotion_blocked")
            for p in pairs
        )
        return render_template(
            "promotion.html",
            promotion=promotion,
            rubric=rubric,
            pair_views=pair_views,
            promotion_blocked=blocked,
        )

    @app.route("/promotions/<promotion_id>/preference", methods=["POST"])
    def save_preference(promotion_id: str):
        safe_path("promotions", promotion_id)
        case_id = request.form.get("case_id", "")
        preference = request.form.get("preference", "")
        notes = request.form.get("notes", "").strip()
        if preference not in ("incumbent", "candidate", "tie"):
            flash("Invalid preference.", "error")
            return redirect(url_for("promotion_detail", promotion_id=promotion_id))
        set_pair_preference(promotion_id, case_id, preference, notes=notes)
        flash(f"Saved preference for {case_id}.", "success")
        return redirect(url_for("promotion_detail", promotion_id=promotion_id))

    @app.route("/promotions/<promotion_id>/approve", methods=["POST"])
    def approve_promotion(promotion_id: str):
        safe_path("promotions", promotion_id)
        promotion = load_promotion(promotion_id)
        try:
            promote_prompt(promotion_id, promotion.candidate_prompt_id)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("promotion_detail", promotion_id=promotion_id))
        flash("Prompt promoted.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/promotions/<promotion_id>/deny", methods=["POST"])
    def deny_promotion_route(promotion_id: str):
        safe_path("promotions", promotion_id)
        rationale = request.form.get("rationale", "").strip()
        deny_promotion(promotion_id, rationale=rationale)
        flash("Promotion denied.", "success")
        return redirect(url_for("dashboard"))

    return app


def _blind_swap(promotion_id: str, case_id: str) -> bool:
    """Deterministic per-case swap so blind A/B order is stable across reloads."""
    digest = hashlib.sha256(f"{promotion_id}:{case_id}".encode()).hexdigest()
    return int(digest[:8], 16) % 2 == 1


def main(host: str = "127.0.0.1", port: int = 5050, debug: bool = False) -> None:
    app = create_app()
    print(f"Supervisor UI: http://{host}:{port}/")
    app.run(host=host, port=port, debug=debug, use_reloader=False)
