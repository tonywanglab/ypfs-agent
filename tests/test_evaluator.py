from __future__ import annotations

import json

import pytest

from harness import evaluator, llm
from harness.checks import run_checks
from harness.models import Checklist, ChecklistItem, Rubric, RubricCriterion


@pytest.fixture()
def rubric():
    return Rubric(
        rubric_id="rubric_v1",
        version=1,
        status="frozen",
        criteria=[
            RubricCriterion(id="options_structure", description="presents options",
                             check_type="llm"),
            RubricCriterion(id="advisory_stance", description="advisory, not directive",
                             check_type="llm"),
            RubricCriterion(id="no_survey_citations", description="no survey cites",
                             check_type="deterministic", deterministic_check="no_survey_citations"),
            RubricCriterion(id="completed_without_error", description="completed cleanly",
                             check_type="deterministic",
                             deterministic_check="completed_without_error"),
        ],
        created_at="t",
    )


def test_generate_checklist_filters_to_llm_criteria_and_valid_ids(monkeypatch, rubric):
    def fake_run_tool_loop(system_prompt, user_msg, model, tools, dispatch_fn, max_steps=6):
        # System prompt should only mention llm criteria ids, not deterministic ones.
        assert "options_structure" in system_prompt
        assert "no_survey_citations" not in system_prompt
        content = json.dumps({
            "items": [
                {"criterion_id": "options_structure", "instruction": "check for 2+ options",
                 "rationale": "r"},
                {"criterion_id": "not_a_real_criterion", "instruction": "ignored", "rationale": "r"},
            ],
            "search_summary": "found some case studies",
        })
        messages = [
            {"role": "assistant", "content": None, "tool_calls": [
                {"id": "c1", "function": {"name": "search_corpus", "arguments": "{}"}}
            ]},
            {"role": "tool", "tool_call_id": "c1",
             "content": json.dumps({"results": [{"doc_id": "vol1_iss1_1"}], "total_found": 1})},
            {"role": "assistant", "content": content},
        ]
        return content, messages

    monkeypatch.setattr(llm, "run_tool_loop", fake_run_tool_loop)

    checklist = evaluator.generate_checklist("some case prompt", "case_1", rubric, "model-x")

    assert checklist.case_id == "case_1"
    assert checklist.rubric_id == "rubric_v1"
    assert len(checklist.items) == 1  # invalid criterion_id filtered out
    assert checklist.items[0].criterion_id == "options_structure"
    assert checklist.evaluator_doc_ids == ["vol1_iss1_1"]
    assert checklist.evaluator_search_summary == "found some case studies"


def test_generate_checklist_signature_has_no_answer_argument():
    import inspect

    params = inspect.signature(evaluator.generate_checklist).parameters
    assert "answer" not in params


def test_generate_checklist_user_message_is_only_the_case_prompt(monkeypatch, rubric):
    captured = {}

    def fake_run_tool_loop(system_prompt, user_msg, model, tools, dispatch_fn, max_steps=6):
        captured["user_msg"] = user_msg
        return json.dumps({"items": [], "search_summary": "s"}), []

    monkeypatch.setattr(llm, "run_tool_loop", fake_run_tool_loop)
    evaluator.generate_checklist("the case prompt", "case_1", rubric, "model-x")

    assert "the case prompt" in captured["user_msg"]
    # No candidate answer text can appear since none was ever passed in.
    assert "candidate" not in captured["user_msg"].lower()


def test_judge_answer_copies_deterministic_verdicts_without_llm_call(monkeypatch, rubric):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("chat_json should not be called when there are no llm checklist items")

    monkeypatch.setattr(llm, "chat_json", fail_if_called)

    answer = "a clean answer with no citations"
    check_results, trace = run_checks(answer, [])

    checklist = Checklist(
        checklist_id="chk_1", case_id="case_1", rubric_id="rubric_v1", model="model-x",
        items=[], evaluator_search_summary="", evaluator_doc_ids=[], created_at="t",
    )

    judgment = evaluator.judge_answer(answer, trace, checklist, rubric, check_results,
                                       run_id="run_1", model="model-x")

    verdict_by_id = {c.criterion_id: c for c in judgment.criteria}
    assert verdict_by_id["no_survey_citations"].source == "deterministic"
    assert verdict_by_id["no_survey_citations"].verdict == "pass"
    assert verdict_by_id["completed_without_error"].verdict == "pass"
    # No llm criteria in judgment since the checklist had no items.
    assert "options_structure" not in verdict_by_id


def test_judge_answer_calls_llm_only_for_checklist_criteria(monkeypatch, rubric):
    captured_payload = {}

    def fake_chat_json(system_prompt, user_prompt, model):
        captured_payload["payload"] = json.loads(user_prompt)
        return {
            "criteria": [
                {"criterion_id": "options_structure", "verdict": "fail",
                 "evidence": "only one option given", "confidence": 0.8},
            ],
            "summary": "weak options coverage",
            "failure_feedback": "add at least one more option",
        }

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)

    answer = "here is a single option"
    check_results, trace = run_checks(answer, [])
    checklist = Checklist(
        checklist_id="chk_1", case_id="case_1", rubric_id="rubric_v1", model="model-x",
        items=[ChecklistItem(id="item_1", criterion_id="options_structure",
                              instruction="check for options", rationale="r")],
        evaluator_search_summary="s", evaluator_doc_ids=[], created_at="t",
    )

    judgment = evaluator.judge_answer(answer, trace, checklist, rubric, check_results,
                                       run_id="run_1", model="model-x")

    verdict_by_id = {c.criterion_id: c for c in judgment.criteria}
    assert verdict_by_id["options_structure"].verdict == "fail"
    assert verdict_by_id["options_structure"].source == "llm"
    assert verdict_by_id["no_survey_citations"].source == "deterministic"
    assert judgment.summary == "weak options coverage"
    assert judgment.failure_feedback == "add at least one more option"
    assert judgment.fail_count() == 1
    # advisory_stance has no checklist item and isn't deterministic, so it's
    # simply absent from this judgment (case-specific scope).
    assert "advisory_stance" not in verdict_by_id
    assert captured_payload["payload"]["agent_answer"] == answer


def test_judge_answer_marks_missing_llm_verdict_as_uncertain(monkeypatch, rubric):
    def fake_chat_json(system_prompt, user_prompt, model):
        return {"criteria": [], "summary": "s", "failure_feedback": ""}

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)

    answer = "answer"
    check_results, trace = run_checks(answer, [])
    checklist = Checklist(
        checklist_id="chk_1", case_id="case_1", rubric_id="rubric_v1", model="model-x",
        items=[ChecklistItem(id="item_1", criterion_id="options_structure",
                              instruction="x", rationale="r")],
        evaluator_search_summary="", evaluator_doc_ids=[], created_at="t",
    )
    judgment = evaluator.judge_answer(answer, trace, checklist, rubric, check_results,
                                       run_id="run_1", model="model-x")
    verdict_by_id = {c.criterion_id: c for c in judgment.criteria}
    assert verdict_by_id["options_structure"].verdict == "uncertain"
    assert verdict_by_id["options_structure"].confidence == 0.0
