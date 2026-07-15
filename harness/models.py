"""Data contracts for the evaluation harness.

Every entity is a small dataclass with `to_dict`/`from_dict` for JSON
round-tripping. Keeping these separate from storage.py and runner.py means
every module agrees on one shape per artifact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


def _from(cls, data: dict):
    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Case:
    """One eval scenario: a fixed prompt run with empty history each time."""

    case_id: str
    prompt: str
    tags: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Case":
        return _from(cls, d)


@dataclass
class RubricCriterion:
    """One persistent criterion in a frozen rubric version.

    check_type="deterministic" criteria are resolved entirely by a named
    function in harness.checks (the judge copies that verdict verbatim).
    check_type="llm" criteria are resolved by the judge model using the
    case-specific checklist item(s) derived from this criterion.
    """

    id: str
    description: str
    check_type: Literal["deterministic", "llm"]
    weight: float = 1.0
    deterministic_check: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "RubricCriterion":
        return _from(cls, d)


@dataclass
class Rubric:
    """A frozen (or proposed) rubric version. Immutable once frozen — updates
    always create a new version, never mutate this one in place."""

    rubric_id: str
    version: int
    status: Literal["frozen", "proposed", "rejected"]
    criteria: list[RubricCriterion]
    created_at: str
    parent_rubric_id: str | None = None
    rationale: str = ""
    derived_from_review_ids: list[str] = field(default_factory=list)
    cycle_id: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Rubric":
        criteria = [RubricCriterion.from_dict(c) for c in d.get("criteria", [])]
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__ and k != "criteria"}
        return cls(criteria=criteria, **kwargs)

    def criterion(self, criterion_id: str) -> RubricCriterion | None:
        return next((c for c in self.criteria if c.id == criterion_id), None)


@dataclass
class PromptVersion:
    """A versioned system-prompt text. version="active" is mirrored onto
    agent/system_prompt.md; other versions live only under evals/prompts/."""

    prompt_id: str
    version: int
    status: Literal["active", "candidate", "archived", "rejected"]
    text: str
    created_at: str
    parent_prompt_id: str | None = None
    rationale: str = ""
    derived_from_review_ids: list[str] = field(default_factory=list)
    cycle_id: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PromptVersion":
        return _from(cls, d)


@dataclass
class CheckResult:
    """One deterministic gate result. hard_failure=True blocks promotion
    regardless of the aggregate judge score, but does not stop judging."""

    check_id: str
    passed: bool
    hard_failure: bool
    evidence: str
    detail: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "CheckResult":
        return _from(cls, d)


@dataclass
class ChecklistItem:
    id: str
    criterion_id: str
    instruction: str
    rationale: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ChecklistItem":
        return _from(cls, d)


@dataclass
class Checklist:
    """Generated from query + frozen rubric BEFORE the candidate answer is
    read. evaluator_doc_ids come from the evaluator's own independent corpus
    search — not from the agent's trace — and are not treated as ground
    truth, only as an independent signal for detecting possible omissions."""

    checklist_id: str
    case_id: str
    rubric_id: str
    model: str
    items: list[ChecklistItem]
    evaluator_search_summary: str
    evaluator_doc_ids: list[str]
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Checklist":
        items = [ChecklistItem.from_dict(i) for i in d.get("items", [])]
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__ and k != "items"}
        return cls(items=items, **kwargs)


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
    def from_dict(cls, d: dict) -> "CriterionVerdict":
        return _from(cls, d)


@dataclass
class Judgment:
    """Judge output: answer + trace + checklist + evaluator search context,
    scored per-criterion. Deterministic criteria are copied in verbatim."""

    judgment_id: str
    run_id: str
    checklist_id: str
    model: str
    criteria: list[CriterionVerdict]
    summary: str
    failure_feedback: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Judgment":
        criteria = [CriterionVerdict.from_dict(c) for c in d.get("criteria", [])]
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__ and k != "criteria"}
        return cls(criteria=criteria, **kwargs)

    def fail_count(self) -> int:
        return sum(1 for c in self.criteria if c.verdict == "fail")


@dataclass
class RunManifest:
    """One agent.run() invocation under a fixed case/prompt/rubric/model."""

    run_id: str
    case_id: str
    role: Literal["incumbent", "candidate", "adhoc"]
    model: str
    prompt_id: str
    rubric_id: str
    created_at: str
    checklist_id: str | None = None
    judgment_id: str | None = None
    promotion_blocked: bool = False
    status: Literal["pending", "checked", "judged"] = "pending"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "RunManifest":
        return _from(cls, d)


@dataclass
class SupervisorReview:
    """The supervisor's read of one run's output + judge assessment. This is
    the ground signal that routes into exactly one update branch."""

    review_id: str
    run_id: str
    verdict: Literal["acceptable", "unacceptable"]
    primary_problem: str
    failure_attribution: Literal[
        "agent_failure", "rubric_gap", "judge_failure", "retrieval_failure", "ambiguous"
    ]
    reviewer: str
    created_at: str
    missing_considerations: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SupervisorReview":
        return _from(cls, d)


@dataclass
class ABPair:
    case_id: str
    incumbent_run_id: str
    candidate_run_id: str
    supervisor_preference: Literal["incumbent", "candidate", "tie"] | None = None
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ABPair":
        return _from(cls, d)


@dataclass
class Promotion:
    """A candidate-prompt A/B campaign against the incumbent, under one
    frozen rubric. Decision is always manual."""

    promotion_id: str
    rubric_id: str
    incumbent_prompt_id: str
    candidate_prompt_id: str
    case_ids: list[str]
    created_at: str
    status: Literal["pending", "approved", "denied"] = "pending"
    decided_at: str | None = None
    rationale: str = ""
    cycle_id: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Promotion":
        return _from(cls, d)
