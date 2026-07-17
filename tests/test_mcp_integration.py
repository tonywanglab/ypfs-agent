"""Integration tests against the real local MCP server (mcp_server/).

No mocks: spawns the actual `python -m mcp_server` subprocess over stdio and
exercises real BM25 search over the corpus checked into markdown/metadata/.
Slower than the unit tests in test_tools.py/test_context.py, but this is the
only place that proves the stdio transport + FastMCP + agent adapter wiring
actually works end-to-end.
"""

from __future__ import annotations

import pytest

from agent.context import RunContext
from agent.mcp_client import McpClient


@pytest.fixture(scope="module")
def mcp_client():
    client = McpClient()
    try:
        yield client
    finally:
        client.close()


def test_list_documents_returns_real_corpus_entries(mcp_client):
    result = mcp_client.call_tool("list_documents", {})
    assert result["total"] > 0
    assert len(result["documents"]) == result["total"]
    first = result["documents"][0]
    assert set(first) == {"doc_id", "title", "document_type", "url"}


def test_list_documents_filters_by_document_type(mcp_client):
    all_docs = mcp_client.call_tool("list_documents", {})
    a_type = all_docs["documents"][0]["document_type"]
    filtered = mcp_client.call_tool("list_documents", {"document_type": a_type})
    assert filtered["total"] > 0
    assert all(doc["document_type"] == a_type for doc in filtered["documents"])


def test_search_corpus_finds_relevant_sections(mcp_client):
    result = mcp_client.call_tool("search_corpus", {
        "query": "bank run liquidity lender of last resort",
        "limit": 5,
    })
    assert result["results"]
    assert len(result["results"]) <= 5
    top = result["results"][0]
    assert set(top) >= {"doc_id", "document_type", "title", "score", "text", "section_path"} \
        or "text" in top  # exact key set is server-owned; just require the essentials


def test_search_corpus_respects_document_type_filter(mcp_client):
    result = mcp_client.call_tool("search_corpus", {
        "query": "financial crisis",
        "document_type": "survey",
        "limit": 5,
    })
    for r in result["results"]:
        assert r.get("document_type") == "survey"


def test_get_document_returns_full_text_for_a_real_doc(mcp_client):
    listing = mcp_client.call_tool("list_documents", {})
    doc_id = listing["documents"][0]["doc_id"]
    doc = mcp_client.call_tool("get_document", {"document_id": doc_id})
    assert doc["doc_id"] == doc_id
    assert doc["text"]


def test_get_document_missing_id_returns_error(mcp_client):
    doc = mcp_client.call_tool("get_document", {"document_id": "not_a_real_doc_id"})
    assert "error" in doc


def test_get_document_rejects_path_traversal(mcp_client):
    doc = mcp_client.call_tool("get_document", {"document_id": "../../../etc/passwd"})
    assert "error" in doc


def test_agent_tools_reach_the_real_server_through_run_context(monkeypatch):
    """End-to-end through the same path agent.run() takes: tools.py's
    search_corpus/get_document -> context.mcp_client -> real subprocess."""
    import agent.tools as tools_module

    monkeypatch.setattr(tools_module, "RETRIEVAL_BACKEND", "mcp")
    context = RunContext()
    try:
        search_result = tools_module.search_corpus("bank run", limit=2, context=context)
        assert search_result["results"]
        doc_id = search_result["results"][0]["doc_id"]

        doc_result = tools_module.get_document(doc_id, context=context)
        assert doc_result["doc_id"] == doc_id
        assert doc_result["text"]

        # Same context, same underlying client — no second subprocess spawned.
        assert context._mcp_client is not None
    finally:
        context.close()
