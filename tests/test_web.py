from __future__ import annotations

import json

import pytest

from harness import candidates, llm, registry, reviews
from harness.models import Case, PromptVersion
import harness.runner as runner
from harness.runner import run_case
from harness.seed import load_cases, seed_all
from harness.storage import atomic_write_json
from harness.web import create_app


@pytest.fixture()
def client(evals_dir, monkeypatch):
    seed_all()

    def fake_agent(user_msg, history=None, model="m", system_prompt=None):
        return "Option A and Option B with tradeoffs.", []

    def fake_checklist(case_prompt, case_id, rubric, model):
        from harness.models import Checklist
        return Checklist(
            checklist_id="chk_ui", case_id=case_id, rubric_id=rubric.rubric_id,
            model=model, items=[], evaluator_search_summary="s",
            evaluator_doc_ids=[], created_at="t",
        )

    def fake_judge(answer, trace, checklist, rubric, check_results, run_id, model):
        from harness.models import CriterionVerdict, Judgment
        return Judgment(
            judgment_id="jud_ui", run_id=run_id, checklist_id=checklist.checklist_id,
            model=model,
            criteria=[CriterionVerdict(criterion_id="options_structure", verdict="fail",
                                       evidence="only one option", source="llm")],
            summary="weak structure", failure_feedback="add more options", created_at="t",
        )

    import harness.runner as runner_mod
    import harness.evaluator as evaluator_mod

    monkeypatch.setattr(runner_mod, "agent_run", fake_agent)
    monkeypatch.setattr(evaluator_mod, "generate_checklist", fake_checklist)
    monkeypatch.setattr(evaluator_mod, "judge_answer", fake_judge)

    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_dashboard_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Supervisor dashboard" in resp.data


def test_run_review_flow(client):
    rubric = candidates.load_rubric(registry.active_rubric_id())
    prompt = candidates.load_prompt(registry.active_prompt_id())
    case = Case(case_id="ui_case", prompt="What should we do?")
    manifest = run_case(case, prompt.text, prompt.prompt_id, "model-x", rubric)

    resp = client.get(f"/runs/{manifest.run_id}")
    assert resp.status_code == 200
    assert b"Option A and Option B" in resp.data

    resp = client.post(f"/runs/{manifest.run_id}/review", data={
        "verdict": "unacceptable",
        "primary_problem": "not enough options",
        "failure_attribution": "agent_failure",
        "notes": "fix prompt",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert reviews.list_reviews()
    assert b"Ready to start prompt" in resp.data or b"Review saved" in resp.data


def test_rubric_proposal_approve_via_web(client, monkeypatch):
    rubric = candidates.load_rubric(registry.active_rubric_id())
    prompt = candidates.load_prompt(registry.active_prompt_id())
    case = Case(case_id="web_rubric", prompt="plan?")
    manifest = run_case(case, prompt.text, prompt.prompt_id, "model-x", rubric)
    review = reviews.create_review(
        manifest.run_id, "unacceptable", "judge wrong", "rubric_gap",
    )

    def fake_chat_json(system, user, model):
        return {
            "rationale": "fix judge",
            "criteria": [
                {"id": "options_structure", "description": "many options", "check_type": "llm"},
            ],
        }

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)

    resp = client.post("/proposals/rubric", data={
        "review_ids": review.review_id,
        "model": "model-x",
    }, follow_redirects=True)
    assert resp.status_code == 200

    proposal = candidates.list_proposals()[0]
    resp = client.post(
        f"/rubrics/proposals/{proposal.rubric_id}/approve",
        data={"criteria_json": json.dumps([c.to_dict() for c in proposal.criteria])},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert registry.active_rubric_id() != "rubric_v1"


def test_invalid_rubric_edit_is_redisplayed(client, monkeypatch):
    registry.lock_cycle("rubric")

    def fake_chat_json(system, user, model):
        return {
            "rationale": "edit me",
            "criteria": [
                {"id": "quality", "description": "good", "check_type": "llm"},
            ],
        }

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)
    proposal = candidates.propose_rubric([], "model-x")
    invalid_edit = '[{"id": "quality", "description": "keep this edit"'

    resp = client.post(
        f"/rubrics/proposals/{proposal.rubric_id}/approve",
        data={"criteria_json": invalid_edit},
    )

    assert resp.status_code == 400
    assert b"keep this edit" in resp.data
    assert candidates.load_proposal(proposal.rubric_id).status == "proposed"


def test_prompt_candidate_can_be_inspected_and_edited(client):
    registry.lock_cycle("prompt")
    cycle_id = registry.load()["cycle"]["cycle_id"]
    candidate = PromptVersion(
        prompt_id="prompt_v2_edit",
        version=2,
        status="candidate",
        text="Original candidate prompt",
        created_at="t",
        parent_prompt_id="prompt_v1",
        cycle_id=cycle_id,
    )
    candidates.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        candidates.CANDIDATES_DIR / f"{candidate.prompt_id}.json",
        candidate.to_dict(),
    )

    detail = client.get(f"/prompts/candidates/{candidate.prompt_id}")
    assert detail.status_code == 200
    assert b"Original candidate prompt" in detail.data

    updated = client.post(
        f"/prompts/candidates/{candidate.prompt_id}/save",
        data={"text": "Revised candidate prompt\n\nWith details."},
        follow_redirects=True,
    )
    assert updated.status_code == 200
    assert b"Revised candidate prompt" in updated.data
    assert candidates.load_prompt_version(candidate.prompt_id).text.startswith(
        "Revised candidate prompt"
    )


def test_prompt_candidate_rejects_empty_edit(client):
    registry.lock_cycle("prompt")
    cycle_id = registry.load()["cycle"]["cycle_id"]
    candidate = PromptVersion(
        prompt_id="prompt_v2_empty",
        version=2,
        status="candidate",
        text="Original candidate prompt",
        created_at="t",
        parent_prompt_id="prompt_v1",
        cycle_id=cycle_id,
    )
    candidates.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        candidates.CANDIDATES_DIR / f"{candidate.prompt_id}.json",
        candidate.to_dict(),
    )

    resp = client.post(
        f"/prompts/candidates/{candidate.prompt_id}/save",
        data={"text": "   "},
    )

    assert resp.status_code == 400
    assert candidates.load_prompt_version(candidate.prompt_id).text == "Original candidate prompt"


def test_candidate_route_does_not_render_active_prompt(client):
    resp = client.get("/prompts/candidates/prompt_v1")
    assert resp.status_code == 404


def test_stale_prompt_candidate_cannot_start_promotion(client):
    registry.lock_cycle("prompt")
    old_cycle_id = registry.load()["cycle"]["cycle_id"]
    candidate = PromptVersion(
        prompt_id="prompt_v2_stale",
        version=2,
        status="candidate",
        text="Stale candidate",
        created_at="t",
        parent_prompt_id="prompt_v1",
        cycle_id=old_cycle_id,
    )
    candidates.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        candidates.CANDIDATES_DIR / f"{candidate.prompt_id}.json",
        candidate.to_dict(),
    )
    registry.close_cycle("cancelled", expected_branch="prompt")
    registry.lock_cycle("prompt", opened_by="new-cycle")

    resp = client.post(
        "/promotions/create",
        data={
            "candidate_prompt_id": candidate.prompt_id,
            "case_ids": load_cases()[0].case_id,
            "model": "model-x",
        },
    )

    assert resp.status_code == 302
    assert runner.list_promotions() == []
    assert registry.locked_branch() == "prompt"


def test_promotion_page_blind_labels(client):
    from harness.models import ABPair, Promotion

    cand = PromptVersion(
        prompt_id="prompt_v2_ui", version=2, status="candidate",
        text="candidate answer text", created_at="t", parent_prompt_id="prompt_v1",
    )
    candidates.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(candidates.CANDIDATES_DIR / f"{cand.prompt_id}.json", cand.to_dict())

    promo_id = "promo_ui"
    promo_dir = runner.PROMOTIONS_DIR / promo_id
    promo_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(promo_dir / "manifest.json", Promotion(
        promotion_id=promo_id, rubric_id="rubric_v1",
        incumbent_prompt_id="prompt_v1", candidate_prompt_id=cand.prompt_id,
        case_ids=["ui_case"], created_at="t",
    ).to_dict())

    for rid, answer, role in [
        ("run_a", "INCUMBENT TEXT", "incumbent"),
        ("run_b", "CANDIDATE TEXT", "candidate"),
    ]:
        rd = runner.RUNS_DIR / rid
        rd.mkdir(parents=True, exist_ok=True)
        atomic_write_json(rd / "manifest.json", {
            "run_id": rid, "case_id": "ui_case", "role": role, "model": "m",
            "prompt_id": "p", "rubric_id": "rubric_v1", "created_at": "t",
            "promotion_blocked": False, "status": "judged",
        })
        atomic_write_json(rd / "case.json", {"case_id": "ui_case", "prompt": "q"})
        atomic_write_json(rd / "answer.json", {"answer": answer})
        atomic_write_json(rd / "trace.json", {})
        atomic_write_json(rd / "checks.json", [])
        atomic_write_json(rd / "checklist.json", {"checklist_id": "c", "items": []})
        atomic_write_json(rd / "judgment.json", {"judgment_id": "j", "criteria": []})

    runner.append_jsonl(promo_dir / "pairs.jsonl", ABPair(
        case_id="ui_case", incumbent_run_id="run_a", candidate_run_id="run_b",
    ).to_dict())

    resp = client.get(f"/promotions/{promo_id}")
    assert resp.status_code == 200
    assert b"Response A" in resp.data
    assert b"INCUMBENT TEXT" in resp.data or b"CANDIDATE TEXT" in resp.data
