"""Per-run dependency container for the agent loop.

A RunContext carries the stateful backends one agent run uses — the RAG
retriever and/or the MCP client, instantiated per context instead of as a
process singleton. It is created when a run starts, shared across that run's
samples, and discarded when the run ends — concurrent runs each get their
own, so session state (e.g. the retriever's embedder-identity check, or one
run's MCP server subprocess) never interleaves across runs. Callers that
create a context are responsible for calling close() when the run ends.

Durable state does not belong here: anything that must survive the run lives
in Postgres (the harness `tasks`/`runs` tables).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

# Which backend agent/tools.py's search_corpus/get_document use: "rag" (the
# Pinecone/pgvector retriever) or "mcp" (the local lexical MCP server in
# mcp_server/). A single env var so it's a one-line flip either way.
RETRIEVAL_BACKEND = os.getenv("RETRIEVAL_BACKEND", "mcp")


@dataclass
class RunContext:
    _retriever: object | None = field(default=None, repr=False)
    _mcp_client: object | None = field(default=None, repr=False)

    @property
    def retriever(self):
        """Lazy per-context retriever — built on first tool use, so contexts
        created for runs that never search don't pay for Pinecone setup."""
        if self._retriever is None:
            from .retrieval import make_retriever
            self._retriever = make_retriever()
        return self._retriever

    @property
    def mcp_client(self):
        """Lazy per-context MCP client — spawns the local server subprocess
        on first tool use, one per run, never shared across concurrent runs."""
        if self._mcp_client is None:
            from .mcp_client import McpClient
            self._mcp_client = McpClient()
        return self._mcp_client

    def close(self) -> None:
        """Release any backend this run actually instantiated. Safe to call
        even if nothing was ever used (no-op)."""
        if self._mcp_client is not None:
            self._mcp_client.close()
