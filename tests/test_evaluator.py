import json

from harness import config, evaluator, llm
from harness.checks import run_checks
from harness.models import Rubric, RubricCriterion


def _rubric():
    return Rubric(
        "rubric_v1",
        1,
        [
            RubricCriterion("options", "presents options", "llm"),
            RubricCriterion("stance", "advisory stance", "llm"),
            RubricCriterion(
                "completed",
                "completed cleanly",
                "deterministic",
                deterministic_check="completed_without_error",
            ),
        ],
        "t",
    )


def test_direct_judge_receives_complete_llm_rubric_and_fixed_model(monkeypatch):
    captured = {}

    def fake_chat_json(system_prompt, user_prompt, model):
        captured["payload"] = json.loads(user_prompt)
        captured["model"] = model
        return {
            "criteria": [
                {
                    "criterion_id": "options",
                    "verdict": "pass",
                    "evidence": "two options",
                    "confidence": 0.9,
                },
                {
                    "criterion_id": "stance",
                    "verdict": "fail",
                    "evidence": "directive",
                    "confidence": 0.8,
                },
            ],
            "summary": "mixed",
            "failure_feedback": "be advisory",
        }

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)
    checks, trace = run_checks("answer", [])
    judgment = evaluator.judge_answer(
        "question", "answer", trace, _rubric(), checks, "run_1"
    )

    assert captured["model"] == config.judge_model()
    assert [item["id"] for item in captured["payload"]["rubric_criteria"]] == [
        "options",
        "stance",
    ]
    assert [verdict.criterion_id for verdict in judgment.criteria] == [
        "options",
        "stance",
        "completed",
    ]
    assert judgment.criteria[-1].source == "deterministic"


def test_missing_or_malformed_judge_rows_become_uncertain(monkeypatch):
    monkeypatch.setattr(llm, "chat_json", lambda **kwargs: {
        "criteria": [
            {"criterion_id": "options", "verdict": "invented", "evidence": "x"},
            {"criterion_id": "unknown", "verdict": "pass", "evidence": "x"},
        ],
        "summary": "",
        "failure_feedback": "",
    })
    checks, trace = run_checks("answer", [])
    judgment = evaluator.judge_answer(
        "question", "answer", trace, _rubric(), checks, "run_1"
    )
    by_id = {item.criterion_id: item for item in judgment.criteria}
    assert by_id["options"].verdict == "uncertain"
    assert by_id["stance"].verdict == "uncertain"
    assert by_id["stance"].confidence == 0.0


def test_unparseable_judge_response_becomes_uncertain(monkeypatch):
    monkeypatch.setattr(
        llm,
        "chat_json",
        lambda **kwargs: (_ for _ in ()).throw(llm.LLMError("not json")),
    )
    checks, trace = run_checks("answer", [])
    judgment = evaluator.judge_answer(
        "question", "answer", trace, _rubric(), checks, "run_1"
    )
    assert [item.verdict for item in judgment.criteria[:2]] == [
        "uncertain",
        "uncertain",
    ]
    assert "malformed" in judgment.summary
