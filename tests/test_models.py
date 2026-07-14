from __future__ import annotations

from harness.models import (
    ABPair,
    Case,
    CheckResult,
    Checklist,
    ChecklistItem,
    CriterionVerdict,
    Judgment,
    Promotion,
    PromptVersion,
    Rubric,
    RubricCriterion,
    RunManifest,
    SupervisorReview,
)


def test_case_roundtrip():
    c = Case(case_id="x", prompt="hello", tags=["a", "b"], notes="n")
    assert Case.from_dict(c.to_dict()) == c


def test_rubric_roundtrip_with_nested_criteria():
    rubric = Rubric(
        rubric_id="rubric_v1",
        version=1,
        status="frozen",
        criteria=[
            RubricCriterion(id="c1", description="d1", check_type="deterministic",
                             deterministic_check="check_x"),
            RubricCriterion(id="c2", description="d2", check_type="llm"),
        ],
        created_at="2026-01-01T00:00:00Z",
    )
    restored = Rubric.from_dict(rubric.to_dict())
    assert restored == rubric
    assert restored.criterion("c1").deterministic_check == "check_x"
    assert restored.criterion("missing") is None


def test_prompt_version_roundtrip():
    p = PromptVersion(prompt_id="prompt_v2", version=2, status="candidate", text="hi",
                       created_at="t", parent_prompt_id="prompt_v1", rationale="r",
                       derived_from_review_ids=["rev_1"])
    assert PromptVersion.from_dict(p.to_dict()) == p


def test_check_result_roundtrip():
    r = CheckResult(check_id="no_survey_citations", passed=False, hard_failure=True,
                     evidence="cited vol7_iss1_3 (survey)", detail={"doc_id": "vol7_iss1_3"})
    assert CheckResult.from_dict(r.to_dict()) == r


def test_checklist_roundtrip_with_items():
    cl = Checklist(
        checklist_id="chk_1",
        case_id="case_1",
        rubric_id="rubric_v1",
        model="m",
        items=[ChecklistItem(id="i1", criterion_id="c1", instruction="do x")],
        evaluator_search_summary="found docs",
        evaluator_doc_ids=["vol1_iss1_2"],
        created_at="t",
    )
    restored = Checklist.from_dict(cl.to_dict())
    assert restored == cl


def test_judgment_roundtrip_and_fail_count():
    j = Judgment(
        judgment_id="j1",
        run_id="run_1",
        checklist_id="chk_1",
        model="m",
        criteria=[
            CriterionVerdict(criterion_id="c1", verdict="fail", evidence="e"),
            CriterionVerdict(criterion_id="c2", verdict="pass", evidence="e"),
        ],
        summary="s",
        failure_feedback="f",
        created_at="t",
    )
    restored = Judgment.from_dict(j.to_dict())
    assert restored == j
    assert restored.fail_count() == 1


def test_run_manifest_roundtrip():
    m = RunManifest(run_id="run_1", case_id="case_1", role="incumbent", model="m",
                     prompt_id="prompt_v1", rubric_id="rubric_v1", created_at="t")
    assert RunManifest.from_dict(m.to_dict()) == m


def test_supervisor_review_roundtrip():
    r = SupervisorReview(
        review_id="rev_1", run_id="run_1", verdict="unacceptable",
        primary_problem="missing option", failure_attribution="agent_failure",
        reviewer="supervisor", created_at="t", missing_considerations=["x"], notes="n",
    )
    assert SupervisorReview.from_dict(r.to_dict()) == r


def test_ab_pair_and_promotion_roundtrip():
    pair = ABPair(case_id="case_1", incumbent_run_id="run_1", candidate_run_id="run_2",
                  supervisor_preference="candidate", notes="better")
    assert ABPair.from_dict(pair.to_dict()) == pair

    promo = Promotion(promotion_id="promo_1", rubric_id="rubric_v1",
                       incumbent_prompt_id="prompt_v1", candidate_prompt_id="prompt_v2",
                       case_ids=["case_1"], created_at="t")
    assert Promotion.from_dict(promo.to_dict()) == promo
