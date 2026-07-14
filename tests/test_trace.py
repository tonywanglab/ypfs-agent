from __future__ import annotations

import json

from harness.trace import build_trace, normalize_messages, tool_summary


def _assistant_call(call_id: str, name: str, arguments: dict) -> dict:
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {"id": call_id, "type": "function",
             "function": {"name": name, "arguments": json.dumps(arguments)}}
        ],
    }


def _tool_result(call_id: str, result: dict) -> dict:
    return {"role": "tool", "tool_call_id": call_id, "content": json.dumps(result)}


def test_normalize_extracts_retrieved_and_fetched_doc_ids():
    messages = [
        {"role": "user", "content": "q"},
        _assistant_call("c1", "search_corpus", {"query": "bank runs"}),
        _tool_result("c1", {"results": [{"doc_id": "vol1_iss1_1", "title": "t"}],
                             "total_found": 1}),
        _assistant_call("c2", "get_document", {"document_id": "vol1_iss1_2"}),
        _tool_result("c2", {"doc_id": "vol1_iss1_2", "text": "full text"}),
        {"role": "assistant", "content": "final answer"},
    ]
    trace = normalize_messages(messages, answer="final answer")
    assert trace.retrieved_doc_ids == {"vol1_iss1_1"}
    assert trace.fetched_doc_ids == {"vol1_iss1_2"}
    assert trace.tool_counts == {"search_corpus": 1, "get_document": 1}
    assert trace.tool_errors == []
    assert trace.hit_max_steps is False


def test_normalize_captures_tool_errors():
    messages = [
        {"role": "user", "content": "q"},
        _assistant_call("c1", "get_document", {"document_id": "../../etc/passwd"}),
        _tool_result("c1", {"error": "Invalid document_id: '../../etc/passwd'"}),
        {"role": "assistant", "content": "done"},
    ]
    trace = normalize_messages(messages, answer="done")
    assert len(trace.tool_errors) == 1
    assert trace.tool_errors[0]["tool_name"] == "get_document"
    assert "Invalid document_id" in trace.tool_errors[0]["error"]
    # An erroring call still counts toward tool_counts / tool_calls, but not
    # toward retrieved/fetched doc_ids.
    assert trace.fetched_doc_ids == set()


def test_normalize_detects_max_steps_sentinel():
    messages = [{"role": "user", "content": "q"}]
    trace = normalize_messages(messages, answer="[stopped: hit MAX_STEPS]")
    assert trace.hit_max_steps is True


def test_normalize_handles_multiple_search_hits_and_no_tool_calls():
    messages = [
        {"role": "user", "content": "q"},
        {"role": "assistant", "content": "no tools needed"},
    ]
    trace = normalize_messages(messages, answer="no tools needed")
    assert trace.tool_calls == []
    assert trace.retrieved_doc_ids == set()
    assert trace.tool_counts == {}


def test_tool_summary_matches_normalize_counts():
    messages = [
        {"role": "user", "content": "q"},
        _assistant_call("c1", "search_corpus", {"query": "x"}),
        _tool_result("c1", {"results": [], "total_found": 0}),
        _assistant_call("c2", "search_corpus", {"query": "y"}),
        _tool_result("c2", {"results": [], "total_found": 0}),
    ]
    assert tool_summary(messages) == {"search_corpus": 2}


def test_build_trace_annotates_tool_names_and_includes_normalized():
    messages = [
        {"role": "user", "content": "q"},
        _assistant_call("c1", "search_corpus", {"query": "x"}),
        _tool_result("c1", {"results": [{"doc_id": "vol2_iss1_1"}], "total_found": 1}),
        {"role": "assistant", "content": "answer with vol2_iss1_1"},
    ]
    built = build_trace(messages, answer="answer with vol2_iss1_1")
    tool_msgs = [m for m in built["messages"] if m["role"] == "tool"]
    assert tool_msgs[0]["name"] == "search_corpus"
    assert built["normalized"]["retrieved_doc_ids"] == ["vol2_iss1_1"]
    assert built["normalized"]["hit_max_steps"] is False
