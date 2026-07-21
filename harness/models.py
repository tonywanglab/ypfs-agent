"""Small JSON-serializable contracts for the evaluation harness."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


def _from(cls, data: dict):
    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Case:
    case_id: str
    prompt: str
    tags: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Case":
        return _from(cls, data)


@dataclass
class PromptVersion:
    prompt_id: str
    version: int
    text: str
    created_at: str
    parent_prompt_id: str | None = None
    rationale: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PromptVersion":
        return _from(cls, data)


@dataclass
class RunManifest:
    run_id: str
    case_id: str
    agent_model: str
    prompt_id: str
    created_at: str
    status: Literal["pending", "complete"] = "pending"
    sample_count: int = 1

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RunManifest":
        # Tolerate pre-simplification manifests while resetting local state.
        migrated = dict(data)
        legacy_model = migrated.get("model", "")
        migrated.setdefault("agent_model", legacy_model)
        migrated.setdefault("sample_count", 1)
        if migrated.get("status") == "judged":
            migrated["status"] = "complete"
        return _from(cls, migrated)


@dataclass
class Feedback:
    feedback_id: str
    run_id: str
    sample_index: int
    selected_text: str
    comment: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Feedback":
        return _from(cls, data)
