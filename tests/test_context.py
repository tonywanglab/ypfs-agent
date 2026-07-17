from __future__ import annotations

from agent.context import RunContext


class _FakeMcpClient:
    instances = 0

    def __init__(self):
        _FakeMcpClient.instances += 1
        self.closed = False

    def close(self):
        self.closed = True


def test_mcp_client_is_lazy_and_reused(monkeypatch):
    import agent.mcp_client as mcp_client_module

    monkeypatch.setattr(mcp_client_module, "McpClient", _FakeMcpClient)
    _FakeMcpClient.instances = 0

    context = RunContext()
    assert _FakeMcpClient.instances == 0

    client_a = context.mcp_client
    client_b = context.mcp_client
    assert _FakeMcpClient.instances == 1
    assert client_a is client_b


def test_close_is_noop_when_nothing_was_instantiated():
    context = RunContext()
    context.close()  # must not raise


def test_close_closes_mcp_client_if_created(monkeypatch):
    import agent.mcp_client as mcp_client_module

    monkeypatch.setattr(mcp_client_module, "McpClient", _FakeMcpClient)
    context = RunContext()
    client = context.mcp_client
    context.close()
    assert client.closed is True


def test_retriever_and_mcp_client_are_independent(monkeypatch):
    import agent.mcp_client as mcp_client_module

    monkeypatch.setattr(mcp_client_module, "McpClient", _FakeMcpClient)

    class _FakeRetriever:
        pass

    import agent.retrieval as retrieval_module
    monkeypatch.setattr(retrieval_module, "make_retriever", _FakeRetriever)

    context = RunContext()
    retriever = context.retriever
    assert isinstance(retriever, _FakeRetriever)
    assert context._mcp_client is None  # untouched until actually used

    client = context.mcp_client
    assert isinstance(client, _FakeMcpClient)
    assert context.retriever is retriever  # unaffected by using the other backend
