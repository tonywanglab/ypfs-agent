from __future__ import annotations

import agent.tools as tools_module
from agent.context import RunContext


class _FakeMcpClient:
    def __init__(self):
        self.calls = []

    def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return {"called": name, "arguments": arguments}


def test_search_corpus_routes_to_mcp_when_backend_is_mcp(monkeypatch):
    monkeypatch.setattr(tools_module, "RETRIEVAL_BACKEND", "mcp")
    context = RunContext()
    fake_client = _FakeMcpClient()
    monkeypatch.setattr(RunContext, "mcp_client", property(lambda self: fake_client))

    result = tools_module.search_corpus("bank runs", document_type="survey", limit=3,
                                        context=context)

    assert result == {
        "called": "search_corpus",
        "arguments": {"query": "bank runs", "document_type": "survey", "limit": 3},
    }
    assert fake_client.calls == [
        ("search_corpus", {"query": "bank runs", "document_type": "survey", "limit": 3}),
    ]


def test_get_document_routes_to_mcp_when_backend_is_mcp(monkeypatch):
    monkeypatch.setattr(tools_module, "RETRIEVAL_BACKEND", "mcp")
    context = RunContext()
    fake_client = _FakeMcpClient()
    monkeypatch.setattr(RunContext, "mcp_client", property(lambda self: fake_client))

    result = tools_module.get_document("vol1_iss1_2", context=context)

    assert result == {
        "called": "get_document",
        "arguments": {"document_id": "vol1_iss1_2"},
    }
    assert fake_client.calls == [("get_document", {"document_id": "vol1_iss1_2"})]


def test_search_corpus_still_uses_rag_when_backend_is_rag(monkeypatch):
    monkeypatch.setattr(tools_module, "RETRIEVAL_BACKEND", "rag")
    captured = {}

    def fake_rag(query, document_type, limit, *, context):
        captured.update(query=query, document_type=document_type, limit=limit)
        return {"results": [], "total_found": 0}

    monkeypatch.setattr(tools_module, "_search_corpus_rag", fake_rag)
    context = RunContext()

    result = tools_module.search_corpus("bank runs", document_type=None, limit=5,
                                        context=context)

    assert result == {"results": [], "total_found": 0}
    assert captured == {"query": "bank runs", "document_type": None, "limit": 5}


def test_get_document_still_uses_rag_when_backend_is_rag(monkeypatch):
    monkeypatch.setattr(tools_module, "RETRIEVAL_BACKEND", "rag")
    captured = {}

    def fake_rag(document_id):
        captured["document_id"] = document_id
        return {"doc_id": document_id}

    monkeypatch.setattr(tools_module, "_get_document_rag", fake_rag)
    context = RunContext()

    result = tools_module.get_document("vol1_iss1_2", context=context)

    assert result == {"doc_id": "vol1_iss1_2"}
    assert captured == {"document_id": "vol1_iss1_2"}


def test_dispatch_surfaces_mcp_startup_failure_as_tool_error(monkeypatch):
    monkeypatch.setattr(tools_module, "RETRIEVAL_BACKEND", "mcp")

    def boom(self):
        raise RuntimeError("mcp server failed to start")

    monkeypatch.setattr(RunContext, "mcp_client", property(boom))

    result = tools_module.dispatch("search_corpus", {"query": "q"})

    assert "error" in result
    assert "mcp server failed to start" in result["error"]
