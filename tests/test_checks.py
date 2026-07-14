from __future__ import annotations

import json

import pytest

from harness.checks import (
    check_citations_resolve,
    check_completed_cleanly,
    check_no_survey_citations,
    extract_cited_doc_ids,
    run_checks,
    any_hard_failure,
)
from harness.trace import normalize_messages


@pytest.fixture()
def metadata_dir(tmp_path):
    d = tmp_path / "metadata"
    d.mkdir()
    (d / "vol1_iss1_1.json").write_text(json.dumps({
        "doc_id": "vol1_iss1_1", "document_type": "case_study", "title": "Case A",
    }))
    (d / "vol7_iss1_3.json").write_text(json.dumps({
        "doc_id": "vol7_iss1_3", "document_type": "survey", "title": "Survey A",
    }))
    return d


def _assistant_call(call_id, name, arguments):
    return {"role": "assistant", "content": None, "tool_calls": [
        {"id": call_id, "type": "function",
         "function": {"name": name, "arguments": json.dumps(arguments)}}
    ]}


def _tool_result(call_id, result):
    return {"role": "tool", "tool_call_id": call_id, "content": json.dumps(result)}


def test_extract_cited_doc_ids_dedupes_and_preserves_order():
    answer = "See vol1_iss1_1 and vol7_iss1_3, also vol1_iss1_1 again."
    assert extract_cited_doc_ids(answer) == ["vol1_iss1_1", "vol7_iss1_3"]


def test_extract_cited_doc_ids_empty_when_no_citations():
    assert extract_cited_doc_ids("no citations here") == []


def test_check_completed_cleanly_passes_on_normal_answer():
    trace = normalize_messages([], answer="a full answer")
    result = check_completed_cleanly("a full answer", trace)
    assert result.passed and not result.hard_failure


def test_check_completed_cleanly_fails_on_max_steps():
    trace = normalize_messages([], answer="[stopped: hit MAX_STEPS]")
    result = check_completed_cleanly("[stopped: hit MAX_STEPS]", trace)
    assert not result.passed and result.hard_failure


def test_check_completed_cleanly_fails_on_empty_answer():
    trace = normalize_messages([], answer="")
    result = check_completed_cleanly("", trace)
    assert not result.passed and result.hard_failure


def test_check_completed_cleanly_fails_on_tool_error():
    messages = [
        _assistant_call("c1", "get_document", {"document_id": "bad"}),
        _tool_result("c1", {"error": "Document not found: bad"}),
    ]
    trace = normalize_messages(messages, answer="answer anyway")
    result = check_completed_cleanly("answer anyway", trace)
    assert not result.passed and result.hard_failure


def test_check_no_survey_citations_passes_with_no_citations(metadata_dir):
    trace = normalize_messages([], answer="no doc_ids here")
    result = check_no_survey_citations("no doc_ids here", trace, metadata_dir)
    assert result.passed


def test_check_no_survey_citations_passes_citing_case_study(metadata_dir):
    trace = normalize_messages([], answer="see vol1_iss1_1")
    result = check_no_survey_citations("see vol1_iss1_1", trace, metadata_dir)
    assert result.passed


def test_check_no_survey_citations_fails_citing_survey(metadata_dir):
    trace = normalize_messages([], answer="per the survey vol7_iss1_3")
    result = check_no_survey_citations("per the survey vol7_iss1_3", trace, metadata_dir)
    assert not result.passed and result.hard_failure
    assert "vol7_iss1_3" in result.evidence


def test_check_citations_resolve_passes_when_retrieved_and_known(metadata_dir):
    messages = [
        _assistant_call("c1", "search_corpus", {"query": "x"}),
        _tool_result("c1", {"results": [{"doc_id": "vol1_iss1_1"}], "total_found": 1}),
    ]
    answer = "as shown in vol1_iss1_1"
    trace = normalize_messages(messages, answer=answer)
    result = check_citations_resolve(answer, trace, metadata_dir)
    assert result.passed


def test_check_citations_resolve_fails_on_unknown_doc_id(metadata_dir):
    answer = "as shown in vol9_iss9_9"
    trace = normalize_messages([], answer=answer)
    result = check_citations_resolve(answer, trace, metadata_dir)
    assert not result.passed and result.hard_failure
    assert "vol9_iss9_9" in result.detail["unknown"]


def test_check_citations_resolve_fails_when_not_retrieved_or_fetched(metadata_dir):
    # vol1_iss1_1 exists in metadata but was never touched by any tool call.
    answer = "as shown in vol1_iss1_1"
    trace = normalize_messages([], answer=answer)
    result = check_citations_resolve(answer, trace, metadata_dir)
    assert not result.passed and result.hard_failure
    assert "vol1_iss1_1" in result.detail["not_in_trace"]


def test_check_citations_resolve_accepts_fetched_via_get_document(metadata_dir):
    messages = [
        _assistant_call("c1", "get_document", {"document_id": "vol1_iss1_1"}),
        _tool_result("c1", {"doc_id": "vol1_iss1_1", "text": "..."}),
    ]
    answer = "per vol1_iss1_1"
    trace = normalize_messages(messages, answer=answer)
    result = check_citations_resolve(answer, trace, metadata_dir)
    assert result.passed


def test_run_checks_returns_all_three_and_trace(metadata_dir):
    messages = [
        _assistant_call("c1", "search_corpus", {"query": "x"}),
        _tool_result("c1", {"results": [{"doc_id": "vol1_iss1_1"}], "total_found": 1}),
    ]
    answer = "per vol1_iss1_1"
    results, trace = run_checks(answer, messages, metadata_dir)
    assert {r.check_id for r in results} == {
        "completed_without_error", "no_survey_citations", "citations_resolve",
    }
    assert all(r.passed for r in results)
    assert trace.retrieved_doc_ids == {"vol1_iss1_1"}


def test_any_hard_failure_true_when_one_fails(metadata_dir):
    messages = []
    answer = "cites vol9_iss9_9 which is unknown"
    results, _ = run_checks(answer, messages, metadata_dir)
    assert any_hard_failure(results) is True


def test_any_hard_failure_false_when_all_pass(metadata_dir):
    results, _ = run_checks("plain answer, no citations", [], metadata_dir)
    assert any_hard_failure(results) is False
