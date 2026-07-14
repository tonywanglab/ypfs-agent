from __future__ import annotations

import pytest

from harness import evaluator, runner
from harness.models import Case, Checklist, CriterionVerdict, Judgment, Rubric, RubricCriterion


@pytest.fixture()
def rubric():
    return Rubric(
        rubric_id="rubric_v1",
        version=1,
        status="frozen",
        criteria=[
            RubricCriterion(id="options_structure", description="d", check_type="llm"),
            RubricCriterion(id="no_survey_citations", description="d", check_type="deterministic",
                             deterministic_check="no_survey_citations"),
        ],
        created_at="t",
    )


@pytest.fixture()
def case():
    return Case(case_id="case_1", prompt="What should the government do?", tags=["plan"])


def _fake_checklist(case_id="case_1", rubric_id="rubric_v1"):
    return Checklist(
        checklist_id="chk_fixed", case_id=case_id, rubric_id=rubric_id, model="model-x",
        items=[], evaluator_search_summary="s", evaluator_doc_ids=[], created_at="t",
    )


def _patch_agent_run(monkeypatch, answer="a clean answer", messages=None):
    def fake_agent_run(user_msg, history=None, model="m", system_prompt=None):
        assert history is None  # every run starts with empty history
        return answer, (messages or [])

    monkeypatch.setattr(runner, "agent_run", fake_agent_run)


def _patch_evaluator(monkeypatch, checklist=None):
    checklist = checklist or _fake_checklist()

    def fake_generate_checklist(case_prompt, case_id, rubric, model):
        return checklist

    def fake_judge_answer(answer, trace, checklist_arg, rubric, check_results, run_id, model):
        return Judgment(
            judgment_id="judg_fixed", run_id=run_id, checklist_id=checklist_arg.checklist_id,
            model=model, criteria=[CriterionVerdict(criterion_id="no_survey_citations",
                                                      verdict="pass", evidence="e",
                                                      source="deterministic")],
            summary="ok", failure_feedback="", created_at="t",
        )

    monkeypatch.setattr(evaluator, "generate_checklist", fake_generate_checklist)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)
    return checklist


def test_run_case_persists_full_bundle(evals_dir, monkeypatch, case, rubric):
    _patch_agent_run(monkeypatch, answer="a clean answer")
    _patch_evaluator(monkeypatch)

    manifest = runner.run_case(case, "prompt text", "prompt_v1", "model-x", rubric, role="adhoc")

    assert manifest.case_id == "case_1"
    assert manifest.role == "adhoc"
    assert manifest.promotion_blocked is False
    assert manifest.status == "judged"

    bundle = runner.load_run_bundle(manifest.run_id)
    assert bundle["answer"] == "a clean answer"
    assert bundle["case"]["case_id"] == "case_1"
    assert bundle["judgment"]["summary"] == "ok"


def test_run_case_marks_promotion_blocked_on_hard_failure(evals_dir, monkeypatch, case, rubric):
    _patch_agent_run(monkeypatch, answer="[stopped: hit MAX_STEPS]")
    _patch_evaluator(monkeypatch)

    manifest = runner.run_case(case, "prompt text", "prompt_v1", "model-x", rubric)
    assert manifest.promotion_blocked is True


def test_run_case_reuses_provided_checklist_without_regenerating(evals_dir, monkeypatch, case, rubric):
    _patch_agent_run(monkeypatch)
    checklist = _fake_checklist()

    def fail_if_called(*args, **kwargs):
        raise AssertionError("generate_checklist should not be called when one is provided")

    def fake_judge_answer(answer, trace, checklist_arg, rubric_arg, check_results, run_id, model):
        return Judgment(judgment_id="judg_fixed", run_id=run_id,
                         checklist_id=checklist_arg.checklist_id, model=model, criteria=[],
                         summary="ok", failure_feedback="", created_at="t")

    monkeypatch.setattr(evaluator, "generate_checklist", fail_if_called)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)

    manifest = runner.run_case(case, "prompt text", "prompt_v1", "model-x", rubric,
                                checklist=checklist)
    assert manifest.checklist_id == "chk_fixed"


def test_run_batch_runs_every_case(evals_dir, monkeypatch, rubric):
    _patch_agent_run(monkeypatch)
    _patch_evaluator(monkeypatch)
    cases = [Case(case_id="c1", prompt="p1"), Case(case_id="c2", prompt="p2")]

    manifests = runner.run_batch(cases, "prompt text", "prompt_v1", "model-x", rubric)
    assert [m.case_id for m in manifests] == ["c1", "c2"]
    assert len(runner.list_runs()) == 2


def test_run_ab_shares_one_checklist_per_case_across_both_sides(evals_dir, monkeypatch, rubric):
    _patch_agent_run(monkeypatch)
    generated_checklists = []

    def fake_generate_checklist(case_prompt, case_id, rubric_arg, model):
        chk = _fake_checklist(case_id=case_id)
        generated_checklists.append(chk)
        return chk

    def fake_judge_answer(answer, trace, checklist_arg, rubric_arg, check_results, run_id, model):
        return Judgment(judgment_id=f"judg_{run_id}", run_id=run_id,
                         checklist_id=checklist_arg.checklist_id, model=model,
                         criteria=[], summary="", failure_feedback="", created_at="t")

    monkeypatch.setattr(evaluator, "generate_checklist", fake_generate_checklist)
    monkeypatch.setattr(evaluator, "judge_answer", fake_judge_answer)

    cases = [Case(case_id="c1", prompt="p1")]
    promotion = runner.run_ab(cases, rubric, "incumbent text", "prompt_v1",
                               "candidate text", "prompt_v2", "model-x")

    assert promotion.status == "pending"
    assert len(generated_checklists) == 1  # exactly one checklist generated for the case

    pairs = runner.load_pairs(promotion.promotion_id)
    assert len(pairs) == 1
    incumbent_manifest = runner.load_manifest(pairs[0].incumbent_run_id)
    candidate_manifest = runner.load_manifest(pairs[0].candidate_run_id)
    assert incumbent_manifest.role == "incumbent"
    assert candidate_manifest.role == "candidate"
    # Both sides were judged against the SAME checklist.
    assert incumbent_manifest.checklist_id == candidate_manifest.checklist_id


def test_set_pair_preference_updates_only_matching_case(evals_dir, monkeypatch, rubric):
    _patch_agent_run(monkeypatch)
    _patch_evaluator(monkeypatch)
    cases = [Case(case_id="c1", prompt="p1"), Case(case_id="c2", prompt="p2")]
    promotion = runner.run_ab(cases, rubric, "incumbent", "prompt_v1", "candidate", "prompt_v2",
                               "model-x")

    runner.set_pair_preference(promotion.promotion_id, "c1", "candidate", notes="better options")
    pairs = {p.case_id: p for p in runner.load_pairs(promotion.promotion_id)}
    assert pairs["c1"].supervisor_preference == "candidate"
    assert pairs["c1"].notes == "better options"
    assert pairs["c2"].supervisor_preference is None


def test_promotion_has_blocked_candidate_run_detects_hard_failure(evals_dir, monkeypatch, rubric):
    call_count = {"n": 0}

    def fake_agent_run(user_msg, history=None, model="m", system_prompt=None):
        call_count["n"] += 1
        # Second call (the candidate side) hits max steps.
        if call_count["n"] == 2:
            return "[stopped: hit MAX_STEPS]", []
        return "fine answer", []

    monkeypatch.setattr(runner, "agent_run", fake_agent_run)
    _patch_evaluator(monkeypatch)

    cases = [Case(case_id="c1", prompt="p1")]
    promotion = runner.run_ab(cases, rubric, "incumbent", "prompt_v1", "candidate", "prompt_v2",
                               "model-x")
    assert runner.promotion_has_blocked_candidate_run(promotion.promotion_id) is True


def test_list_promotions_returns_all(evals_dir, monkeypatch, rubric):
    _patch_agent_run(monkeypatch)
    _patch_evaluator(monkeypatch)
    cases = [Case(case_id="c1", prompt="p1")]
    runner.run_ab(cases, rubric, "incumbent", "prompt_v1", "candidate", "prompt_v2", "model-x")
    runner.run_ab(cases, rubric, "incumbent", "prompt_v1", "candidate", "prompt_v3", "model-x")
    assert len(runner.list_promotions()) == 2
