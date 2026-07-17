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
class RubricCriterion:
    id: str
    description: str
    check_type: Literal["deterministic", "llm"]
    weight: float = 1.0
    deterministic_check: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RubricCriterion":
        return _from(cls, data)


@dataclass
class RubricVersion:
    rubric_id: str
    version: int
    criteria: list[RubricCriterion]
    created_at: str
    parent_rubric_id: str | None = None
    rationale: str = ""
    derived_from_review_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RubricVersion":
        criteria = [RubricCriterion.from_dict(c) for c in data.get("criteria", [])]
        kwargs = {
            k: v
            for k, v in data.items()
            if k in cls.__dataclass_fields__ and k != "criteria"
        }
        return cls(criteria=criteria, **kwargs)


@dataclass
class PromptVersion:
    prompt_id: str
    version: int
    text: str
    created_at: str
    parent_prompt_id: str | None = None
    rationale: str = ""
    derived_from_review_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PromptVersion":
        return _from(cls, data)


@dataclass
class CheckResult:
    check_id: str
    passed: bool
    hard_failure: bool
    evidence: str
    detail: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CheckResult":
        return _from(cls, data)


@dataclass
class CriterionVerdict:
    criterion_id: str
    verdict: Literal["pass", "fail", "uncertain"]
    evidence: str
    confidence: float = 1.0
    source: Literal["deterministic", "llm"] = "llm"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CriterionVerdict":
        return _from(cls, data)


@dataclass
class Judgment:
    judgment_id: str
    run_id: str
    model: str
    criteria: list[CriterionVerdict]
    summary: str
    failure_feedback: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Judgment":
        criteria = [CriterionVerdict.from_dict(c) for c in data.get("criteria", [])]
        kwargs = {
            k: v
            for k, v in data.items()
            if k in cls.__dataclass_fields__ and k != "criteria"
        }
        return cls(criteria=criteria, **kwargs)

    def fail_count(self) -> int:
        return sum(1 for criterion in self.criteria if criterion.verdict == "fail")


@dataclass
class RunManifest:
    run_id: str
    case_id: str
    agent_model: str
    judge_model: str
    prompt_id: str
    rubric_id: str
    created_at: str
    judgment_id: str | None = None
    hard_failure: bool = False
    status: Literal["pending", "judged"] = "pending"
    sample_count: int = 1

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RunManifest":
        # Tolerate pre-simplification manifests while resetting local state.
        migrated = dict(data)
        legacy_model = migrated.get("model", "")
        migrated.setdefault("agent_model", legacy_model)
        migrated.setdefault("judge_model", legacy_model)
        migrated.setdefault("hard_failure", migrated.get("promotion_blocked", False))
        migrated.setdefault("sample_count", 1)
        return _from(cls, migrated)


ReviewTarget = Literal["prompt_issue", "rubric_issue", "invalid_run"]


@dataclass
class SupervisorReview:
    review_id: str
    run_id: str
    verdict: Literal["acceptable", "unacceptable"]
    primary_problem: str
    failure_attribution: ReviewTarget | None
    reviewer: str
    created_at: str
    missing_considerations: list[str] = field(default_factory=list)
    notes: str = ""
    status: Literal["open", "used"] = "open"
    used_by_version_id: str | None = None
    used_at: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SupervisorReview":
        migrated = dict(data)
        legacy = migrated.get("failure_attribution")
        migrated["failure_attribution"] = {
            "agent_failure": "prompt_issue",
            "rubric_gap": "rubric_issue",
            "judge_failure": "rubric_issue",
            "retrieval_failure": "invalid_run",
            "ambiguous": "invalid_run",
        }.get(legacy, legacy)
        migrated.setdefault("status", "open")
        if migrated.get("status") not in ("open", "used"):
            migrated["status"] = "open"
        migrated.setdefault("used_by_version_id", None)
        migrated.setdefault("used_at", None)
        return _from(cls, migrated)
