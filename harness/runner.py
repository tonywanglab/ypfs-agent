"""Batch runner: agent.run() -> deterministic checks -> checklist -> judgment,
all persisted under evals/runs/{run_id}/.

Every case runs with EMPTY history and a fixed (prompt_text, model, rubric)
triple — no memory carried between cases or between incumbent/candidate
runs in an A/B pair, so comparisons stay repeatable.
"""

from __future__ import annotations

from agent.agent import run as agent_run

from . import evaluator, registry
from .checks import any_hard_failure, run_checks
from .models import ABPair, Case, Checklist, Promotion, RunManifest, Rubric
from .storage import (
    EVALS_DIR,
    append_jsonl,
    atomic_write_json,
    new_id,
    now_iso,
    read_json,
    read_jsonl,
    rewrite_jsonl,
)
from .trace import build_trace

RUNS_DIR = EVALS_DIR / "runs"
PROMOTIONS_DIR = EVALS_DIR / "promotions"


def _run_dir(run_id: str):
    return RUNS_DIR / run_id


def save_manifest(manifest: RunManifest) -> None:
    atomic_write_json(_run_dir(manifest.run_id) / "manifest.json", manifest.to_dict())


def load_manifest(run_id: str) -> RunManifest:
    return RunManifest.from_dict(read_json(_run_dir(run_id) / "manifest.json"))


def load_run_bundle(run_id: str) -> dict:
    """Everything persisted for one run: case, answer, trace, checks,
    checklist, judgment, manifest."""
    d = _run_dir(run_id)
    return {
        "manifest": read_json(d / "manifest.json"),
        "case": read_json(d / "case.json"),
        "answer": read_json(d / "answer.json")["answer"],
        "trace": read_json(d / "trace.json"),
        "checks": read_json(d / "checks.json"),
        "checklist": read_json(d / "checklist.json"),
        "judgment": read_json(d / "judgment.json"),
    }


def list_runs() -> list[RunManifest]:
    if not RUNS_DIR.exists():
        return []
    manifests = []
    for d in sorted(RUNS_DIR.iterdir()):
        mpath = d / "manifest.json"
        if mpath.exists():
            manifests.append(RunManifest.from_dict(read_json(mpath)))
    return manifests


def run_case(case: Case, prompt_text: str, prompt_id: str, model: str, rubric: Rubric, *,
             role: str = "adhoc", checklist: Checklist | None = None) -> RunManifest:
    """Run one case through agent.run() with fresh history, then check +
    judge it.

    If `checklist` is not provided, one is generated fresh (evaluator call
    1). Passing a pre-generated checklist lets an A/B run reuse the SAME
    checklist for both the incumbent and the candidate, since the checklist
    depends only on (case, rubric) — never on which prompt produced the
    answer being judged.
    """
    run_id = new_id("run")

    answer, messages = agent_run(case.prompt, history=None, model=model, system_prompt=prompt_text)

    check_results, trace = run_checks(answer, messages)
    blocked = any_hard_failure(check_results)

    if checklist is None:
        checklist = evaluator.generate_checklist(case.prompt, case.case_id, rubric, model)

    judgment = evaluator.judge_answer(
        answer, trace, checklist, rubric, check_results, run_id=run_id, model=model,
    )

    manifest = RunManifest(
        run_id=run_id, case_id=case.case_id, role=role, model=model,
        prompt_id=prompt_id, rubric_id=rubric.rubric_id,
        checklist_id=checklist.checklist_id, judgment_id=judgment.judgment_id,
        created_at=now_iso(), promotion_blocked=blocked, status="judged",
    )

    run_dir = _run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(run_dir / "case.json", case.to_dict())
    atomic_write_json(run_dir / "answer.json", {"answer": answer})
    atomic_write_json(run_dir / "trace.json", build_trace(messages, answer))
    atomic_write_json(run_dir / "checks.json", [r.to_dict() for r in check_results])
    atomic_write_json(run_dir / "checklist.json", checklist.to_dict())
    atomic_write_json(run_dir / "judgment.json", judgment.to_dict())
    save_manifest(manifest)

    return manifest


def run_batch(cases: list[Case], prompt_text: str, prompt_id: str, model: str, rubric: Rubric,
              *, role: str = "adhoc") -> list[RunManifest]:
    return [run_case(c, prompt_text, prompt_id, model, rubric, role=role) for c in cases]


def _promo_dir(promotion_id: str):
    return PROMOTIONS_DIR / promotion_id


def run_ab(cases: list[Case], rubric: Rubric, incumbent_prompt_text: str, incumbent_prompt_id: str,
           candidate_prompt_text: str, candidate_prompt_id: str, model: str,
           *, cycle_id: str | None = None) -> Promotion:
    """Run every case under both prompts, sharing one checklist per case so
    the same case-specific criteria apply to both sides. Decision is always
    left to the supervisor — this only produces material to review."""
    if cycle_id is not None:
        registry.require_cycle("prompt", cycle_id=cycle_id)
        if registry.active_prompt_id() != incumbent_prompt_id:
            raise ValueError("Promotion incumbent is no longer the active prompt")

    promotion_id = new_id("promo")
    pairs: list[ABPair] = []

    for case in cases:
        checklist = evaluator.generate_checklist(case.prompt, case.case_id, rubric, model)
        incumbent = run_case(case, incumbent_prompt_text, incumbent_prompt_id, model, rubric,
                              role="incumbent", checklist=checklist)
        candidate = run_case(case, candidate_prompt_text, candidate_prompt_id, model, rubric,
                              role="candidate", checklist=checklist)
        pairs.append(ABPair(case_id=case.case_id, incumbent_run_id=incumbent.run_id,
                             candidate_run_id=candidate.run_id))

    if cycle_id is not None:
        registry.require_cycle("prompt", cycle_id=cycle_id)
        if registry.active_prompt_id() != incumbent_prompt_id:
            raise ValueError("Prompt cycle changed while the A/B campaign was running")

    promotion = Promotion(
        promotion_id=promotion_id, rubric_id=rubric.rubric_id,
        incumbent_prompt_id=incumbent_prompt_id, candidate_prompt_id=candidate_prompt_id,
        case_ids=[c.case_id for c in cases], created_at=now_iso(), status="pending",
        cycle_id=cycle_id,
    )

    promo_dir = _promo_dir(promotion_id)
    atomic_write_json(promo_dir / "manifest.json", promotion.to_dict())
    for pair in pairs:
        append_jsonl(promo_dir / "pairs.jsonl", pair.to_dict())

    return promotion


def load_promotion(promotion_id: str) -> Promotion:
    return Promotion.from_dict(read_json(_promo_dir(promotion_id) / "manifest.json"))


def save_promotion(promotion: Promotion) -> None:
    atomic_write_json(_promo_dir(promotion.promotion_id) / "manifest.json", promotion.to_dict())


def load_pairs(promotion_id: str) -> list[ABPair]:
    return [ABPair.from_dict(d) for d in read_jsonl(_promo_dir(promotion_id) / "pairs.jsonl")]


def save_pairs(promotion_id: str, pairs: list[ABPair]) -> None:
    rewrite_jsonl(_promo_dir(promotion_id) / "pairs.jsonl", [p.to_dict() for p in pairs])


def set_pair_preference(promotion_id: str, case_id: str, preference: str, notes: str = "") -> None:
    pairs = load_pairs(promotion_id)
    for p in pairs:
        if p.case_id == case_id:
            p.supervisor_preference = preference
            p.notes = notes
    save_pairs(promotion_id, pairs)


def list_promotions() -> list[Promotion]:
    if not PROMOTIONS_DIR.exists():
        return []
    out = []
    for d in sorted(PROMOTIONS_DIR.iterdir()):
        mpath = d / "manifest.json"
        if mpath.exists():
            out.append(Promotion.from_dict(read_json(mpath)))
    return out


def promotion_has_blocked_candidate_run(promotion_id: str) -> bool:
    """True if any candidate-side run in this promotion hit a deterministic
    hard failure. Used to gate promotion regardless of judge scores."""
    for pair in load_pairs(promotion_id):
        manifest = load_manifest(pair.candidate_run_id)
        if manifest.promotion_blocked:
            return True
    return False
