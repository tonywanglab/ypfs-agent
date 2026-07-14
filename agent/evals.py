"""
Eval-driven development harness.

Thin wrapper over harness.runner for running versioned cases against the
active prompt and rubric. The legacy Case/check API remains for simple
boolean smoke tests.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

from .agent import DEFAULT_MODEL, run

from harness import registry
from harness.candidates import load_prompt, load_rubric
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
    model: str | None = None,
    *,
    role: str = "adhoc",
) -> list[dict]:
    """Run harness cases with the active prompt/rubric and return manifests."""
    model = model or os.environ.get("AGENT_MODEL", DEFAULT_MODEL)
    rubric = load_rubric(registry.active_rubric_id())
    prompt = load_prompt(registry.active_prompt_id())
    cases = load_cases()
    if case_ids:
        wanted = set(case_ids)
        cases = [c for c in cases if c.case_id in wanted]
    manifests = run_batch(cases, prompt.text, prompt.prompt_id, model, rubric, role=role)
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
