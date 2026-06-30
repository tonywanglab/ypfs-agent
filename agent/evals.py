"""
Eval-driven development harness

- a Case is an input plus a check over the agent's output AND trace
- `agent.run` returns (answer, messages)
    - check can assert on 
        - the final text
        - whether a tool was called
        - on which doc_ids were retrieved

Because run() takes `model`, the same Case set runs across any list of
OpenRouter slugs — model comparison is a loop over models, no code changes.
"""

from dataclasses import dataclass
from typing import Callable
from .agent import run, DEFAULT_MODEL

# (answer, messages) -> passed?   messages is the full trace w/ tool turns
Check = Callable[[str, list], bool]


@dataclass
class Case:
    name: str
    user_msg: str
    check: Check


CASES: list[Case] = [
    # Example — uncomment and adapt:
    # Case(
    #     name="retrieves_before_answering",
    #     user_msg="What interventions stopped bank runs in the 2008 crisis?",
    #     check=lambda answer, messages: any(m.get("role") == "tool" for m in messages),
    # ),
]


def run_evals(cases: list[Case] = CASES, model: str | None = None) -> None:
    """Run each case through agent.run and report pass/fail

    TODO (you write this):
      - for each case: answer, messages = run(case.user_msg, model=model or DEFAULT_MODEL)
      - record case.check(answer, messages); collect failures
      - print a summary (passed/total) and the failing case names
    """
    passed_count = 0
    failures = []
    for case in cases:
        answer, messages = run(case.user_msg, model=model if model else DEFAULT_MODEL)
        if case.check(answer, messages):
            passed_count += 1
        else: # fail
            failures.append(case)
    print(f'{passed_count}/{len(cases)} with failing case names {", ".join(case.name for case in failures)})')