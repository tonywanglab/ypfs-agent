"""Per-run dependency container for the agent loop.

A RunContext carries the stateful backends one agent run uses (today the
retriever; a future MCP backend would ride here too, instantiated per context
instead of as a process singleton). It is created when a run starts, shared
across that run's samples, and discarded when the run ends — concurrent runs
each get their own, so session state (e.g. the retriever's embedder-identity
check) never interleaves across runs.

Durable state does not belong here: anything that must survive the run lives
in Postgres (the harness `tasks`/`runs` tables).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RunContext:
    _retriever: object | None = field(default=None, repr=False)

    @property
    def retriever(self):
        """Lazy per-context retriever — built on first tool use, so contexts
        created for runs that never search don't pay for Pinecone setup."""
        if self._retriever is None:
            from .retrieval import make_retriever
            self._retriever = make_retriever()
        return self._retriever
