from harness.models import (
    Case,
    CriterionVerdict,
    Judgment,
    PromptVersion,
    Rubric,
    RubricCriterion,
    RunManifest,
    SupervisorReview,
)


def test_version_and_run_contracts_roundtrip():
    prompt = PromptVersion("prompt_v1", 1, "text", "t")
    rubric = Rubric(
        "rubric_v1",
        1,
        [RubricCriterion("quality", "good answer", "llm")],
        "t",
    )
    manifest = RunManifest(
        "run_1",
        "case_1",
        "anthropic/claude-fable-5",
        "openai/gpt-5.6-terra",
        prompt.prompt_id,
        rubric.rubric_id,
        "t",
    )
    assert PromptVersion.from_dict(prompt.to_dict()) == prompt
    assert Rubric.from_dict(rubric.to_dict()) == rubric
    assert RunManifest.from_dict(manifest.to_dict()) == manifest


def test_judgment_roundtrip_and_fail_count():
    judgment = Judgment(
        "judg_1",
        "run_1",
        "openai/gpt-5.6-terra",
        [
            CriterionVerdict("one", "fail", "missing"),
            CriterionVerdict("two", "pass", "present"),
        ],
        "summary",
        "feedback",
        "t",
    )
    restored = Judgment.from_dict(judgment.to_dict())
    assert restored == judgment
    assert restored.fail_count() == 1


def test_review_contract_uses_three_targets_and_no_target_for_acceptable():
    review = SupervisorReview(
        "rev_1",
        "run_1",
        "unacceptable",
        "wrong behavior",
        "prompt_issue",
        "supervisor",
        "t",
    )
    assert SupervisorReview.from_dict(review.to_dict()) == review
    assert SupervisorReview.from_dict({
        **review.to_dict(),
        "failure_attribution": "rubric_gap",
    }).failure_attribution == "rubric_issue"


def test_case_roundtrip():
    case = Case("case_1", "question", ["plan"], "notes")
    assert Case.from_dict(case.to_dict()) == case
