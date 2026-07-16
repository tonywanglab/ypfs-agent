"""
Eval-driven development harness.

Thin wrapper over harness.runner for running versioned cases against an
explicit prompt/rubric pair. The legacy Case/check API remains for simple
boolean smoke tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .agent import DEFAULT_MODEL, run

from harness import versions
from harness.runner import run_batch
from harness.seed import load_cases

# (answer, messages) -> passed?
Check = Callable[[str, list], bool]


@dataclass
class Case:
    name: str
    user_msg: str
    check: Check


CASES: list[Case] = []


def run_harness_evals(
    case_ids: list[str] | None = None,
    prompt_id: str | None = None,
    rubric_id: str | None = None,
) -> list[dict]:
    """Run cases using explicit versions, defaulting to the latest files."""
    prompt = versions.load_prompt(prompt_id) if prompt_id else versions.latest_prompt()
    rubric = versions.load_rubric(rubric_id) if rubric_id else versions.latest_rubric()
    cases = load_cases()
    if case_ids:
        wanted = set(case_ids)
        cases = [c for c in cases if c.case_id in wanted]
    manifests = run_batch(cases, prompt.text, prompt.prompt_id, rubric)
    return [m.to_dict() for m in manifests]


def run_evals(cases: list[Case] = CASES, model: str | None = None) -> None:
    """Legacy boolean eval loop over inline Case objects."""
    passed_count = 0
    failures = []
    resolved_model = model if model else DEFAULT_MODEL
    for case in cases:
        answer, messages = run(case.user_msg, model=resolved_model)
        if case.check(answer, messages):
            passed_count += 1
        else:
            failures.append(case)
    print(
        f"{passed_count}/{len(cases)} passed"
        + (f"; failures: {', '.join(c.name for c in failures)}" if failures else "")
    )
