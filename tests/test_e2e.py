"""End-to-end workflow: run -> review -> rubric proposal -> approve -> cycle lock."""

from __future__ import annotations

import pytest

from harness import candidates, llm, registry, reviews
from harness.models import Case, CriterionVerdict, Judgment, Rubric, RubricCriterion
from harness.runner import run_case
from harness.seed import seed_all


def _patch_run_pipeline(monkeypatch):
    def fake_agent(user_msg, history=None, model="m", system_prompt=None):
        return "single option only", []

    def fake_checklist(case_prompt, case_id, rubric, model):
        from harness.models import Checklist
        return Checklist(
            checklist_id="chk_e2e", case_id=case_id, rubric_id=rubric.rubric_id,
            model=model, items=[], evaluator_search_summary="", evaluator_doc_ids=[],
            created_at="t",
        )

    def fake_judge(answer, trace, checklist, rubric, check_results, run_id, model):
        return Judgment(
            judgment_id="jud_e2e", run_id=run_id, checklist_id=checklist.checklist_id,
            model=model,
            criteria=[CriterionVerdict(criterion_id="options_structure", verdict="fail",
                                       evidence="e", source="llm")],
            summary="bad", failure_feedback="rubric missed multi-option requirement", created_at="t",
        )

    def fake_rubric_llm(system, user, model):
        return {
            "rationale": "emphasize options",
            "criteria": [
                {"id": "options_structure", "description": ">=3 named options", "check_type": "llm"},
                {"id": "no_survey_citations", "description": "no surveys", "check_type": "deterministic",
                 "deterministic_check": "no_survey_citations"},
            ],
        }

    import harness.runner as runner_mod
    import harness.evaluator as evaluator_mod

    monkeypatch.setattr(runner_mod, "agent_run", fake_agent)
    monkeypatch.setattr(evaluator_mod, "generate_checklist", fake_checklist)
    monkeypatch.setattr(evaluator_mod, "judge_answer", fake_judge)
    monkeypatch.setattr(llm, "chat_json", fake_rubric_llm)


def test_e2e_rubric_cycle(evals_dir, monkeypatch):
    _patch_run_pipeline(monkeypatch)
    seed_all()

    rubric = candidates.load_rubric(registry.active_rubric_id())
    prompt = candidates.load_prompt(registry.active_prompt_id())
    case = Case(case_id="e2e_case", prompt="Recommend a plan.")

    manifest = run_case(case, prompt.text, prompt.prompt_id, "model-x", rubric)
    assert manifest.status == "judged"

    review = reviews.create_review(
        manifest.run_id, verdict="unacceptable", primary_problem="rubric gap",
        failure_attribution="rubric_gap",
    )
    from harness import router
    assert router.route_review(review)["branch"] == "rubric"

    proposal = candidates.propose_rubric([review.review_id], "model-x")
    assert registry.locked_branch() == "rubric"

    with pytest.raises(registry.CycleLockedError):
        candidates.propose_prompt([review.review_id], "model-x")

    frozen = candidates.approve_rubric(proposal.rubric_id)
    assert frozen.rubric_id == registry.active_rubric_id()
    assert registry.locked_branch() is None

    # Next cycle: prompt branch can open.
    registry.lock_cycle("prompt")
    assert registry.locked_branch() == "prompt"
