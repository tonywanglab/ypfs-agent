"""JSON-serializable contracts for the chat tables.

Mirrors harness/models.py's style (dataclass + to_dict/from_dict, tolerant of
extra columns) but lives here so the shared module takes no diff.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


def _from(cls, data: dict):
    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Conversation:
    conversation_id: str
    title: str
    role: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        return _from(cls, data)


@dataclass
class Turn:
    """One question. `query` is what the person typed; `quoted_text` is the span
    they had selected in an earlier response when they typed it.

    The two are combined by conversations.compose_message() into the text the
    model actually sees — the quote is part of the question, not an annotation
    hanging off the previous answer.
    """

    turn_id: str
    conversation_id: str
    turn_index: int
    query: str
    quoted_text: str | None
    quoted_run_id: str | None
    stale: bool
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Turn":
        return _from(cls, data)


@dataclass
class PromptRevision:
    """A system-prompt revision the agent proposed via its admin-only tool.

    `to_prompt_id` stays None until an admin accepts, at which point the text is
    committed through versions.save_prompt() as the next immutable prompt_vN.
    """

    revision_id: str
    conversation_id: str
    source_turn_id: str | None
    source_run_id: str | None
    from_prompt_id: str
    to_prompt_id: str | None
    proposed_text: str
    rationale: str
    status: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PromptRevision":
        return _from(cls, data)


@dataclass
class GoldenPair:
    """An admin-marked reference example. query/answer are snapshots, so
    regenerating the turn they came from never mutates the dataset row."""

    golden_id: str
    conversation_id: str
    turn_id: str
    run_id: str
    query: str
    answer: str
    prompt_id: str
    agent_model: str
    note: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GoldenPair":
        return _from(cls, data)
