"""Run the fixed agent, deterministic checks, and direct fixed judge.

Persistence is Postgres: one `runs` row per run (inserted at start with
status='pending' so a crashed run stays inspectable, finalized to 'judged')
and one `run_samples` row per sample as it completes.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from agent.agent import run as agent_run
from agent.context import RunContext

from . import config, dbio, evaluator, seed
from .checks import any_hard_failure, run_checks
from .models import Case, RunManifest, RubricVersion
from .storage import new_id, now_iso
from .trace import build_trace

RunPhase = Literal["prepare", "agent", "checks", "judge", "sample_done"]
ProgressCallback = Callable[[RunPhase, int, int, str], None]


def any_hard_failure_from_dicts(checks: list[dict]) -> bool:
    return any(c.get("hard_failure") and not c.get("passed") for c in checks)


def _manifest_from_row(row: dict) -> RunManifest:
    return RunManifest.from_dict(row)


def save_manifest(manifest: RunManifest, case_snapshot: dict | None = None) -> None:
    """Upsert the run row. case_snapshot is required on first insert; on
    conflict only the mutable outcome fields are updated."""
    dbio.execute(
        """
        INSERT INTO runs (run_id, case_id, case_snapshot, prompt_id, rubric_id,
                          agent_model, judge_model, judgment_id, hard_failure,
                          status, sample_count, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (run_id) DO UPDATE SET
            judgment_id = EXCLUDED.judgment_id,
            hard_failure = EXCLUDED.hard_failure,
            status = EXCLUDED.status,
            sample_count = EXCLUDED.sample_count
        """,
        (manifest.run_id, manifest.case_id, dbio.jsonb(case_snapshot or {}),
         manifest.prompt_id, manifest.rubric_id, manifest.agent_model,
         manifest.judge_model, manifest.judgment_id, manifest.hard_failure,
         manifest.status, manifest.sample_count, manifest.created_at),
    )


def load_manifest(run_id: str) -> RunManifest:
    row = dbio.q1("SELECT * FROM runs WHERE run_id = %s", (run_id,))
    if row is None:
        raise FileNotFoundError(f"Run {run_id!r} does not exist")
    return _manifest_from_row(row)


def load_run_bundle(run_id: str) -> dict:
    run_row = dbio.q1("SELECT * FROM runs WHERE run_id = %s", (run_id,))
    if run_row is None:
        raise FileNotFoundError(f"Run {run_id!r} does not exist")
    sample_rows = dbio.q(
        "SELECT * FROM run_samples WHERE run_id = %s ORDER BY sample_index",
        (run_id,),
    )
    if not sample_rows:
        raise FileNotFoundError(f"Run {run_id!r} has no sample artifacts")

    samples = [
        {
            "index": row["sample_index"],
            "answer": row["answer"],
            "trace": row["trace"],
            "checks": row["checks"],
            "judgment": row["judgment"],
            "hard_failure": row["hard_failure"],
        }
        for row in sample_rows
    ]
    manifest = _manifest_from_row(run_row).to_dict()
    first = samples[0]
    return {
        "manifest": manifest,
        "case": run_row["case_snapshot"],
        "samples": samples,
        "answer": first["answer"],
        "trace": first["trace"],
        "checks": first["checks"],
        "judgment": first["judgment"],
    }


def list_runs() -> list[RunManifest]:
    rows = dbio.q("SELECT * FROM runs ORDER BY created_at, run_id")
    return [_manifest_from_row(row) for row in rows]


def delete_run(run_id: str) -> None:
    # Samples cascade; tasks referencing the run get run_id set NULL.
    deleted = dbio.execute("DELETE FROM runs WHERE run_id = %s", (run_id,))
    if not deleted:
        raise FileNotFoundError(f"Run {run_id!r} does not exist")


def _execute_sample(
    *,
    case: Case,
    prompt_text: str,
    prompt_id: str,
    rubric: RubricVersion,
    run_id: str,
    sample_index: int,
    sample_total: int,
    on_progress: ProgressCallback | None = None,
    context: RunContext | None = None,
) -> tuple[list, bool, object]:
    def report(phase: RunPhase) -> None:
        if on_progress:
            on_progress(phase, sample_index, sample_total, run_id)

    report("agent")
    agent_model = config.agent_model()
    answer, messages = agent_run(
        case.prompt,
        history=None,
        model=agent_model,
        system_prompt=prompt_text,
        context=context,
    )
    report("checks")
    check_results, normalized_trace = run_checks(answer, messages)
    report("judge")
    judgment = evaluator.judge_answer(
        case_prompt=case.prompt,
        answer=answer,
        normalized_trace=normalized_trace,
        rubric=rubric,
        check_results=check_results,
        run_id=run_id,
    )
    hard_failure = any_hard_failure(check_results)
    dbio.execute(
        """
        INSERT INTO run_samples (run_id, sample_index, answer, trace, checks,
                                 judgment, hard_failure)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (run_id, sample_index, answer,
         dbio.jsonb(build_trace(messages, answer)),
         dbio.jsonb([result.to_dict() for result in check_results]),
         dbio.jsonb(judgment.to_dict()), hard_failure),
    )
    return check_results, hard_failure, judgment


def run_case_samples(
    case: Case,
    prompt_text: str,
    prompt_id: str,
    rubric: RubricVersion,
    samples: int = 1,
    on_progress: ProgressCallback | None = None,
    context: RunContext | None = None,
) -> RunManifest:
    samples = max(1, min(samples, 20))
    run_id = new_id("run")
    agent_model = config.agent_model()
    judge_model = config.judge_model()

    # The runs row needs its case FK; an unknown case at this point is by
    # definition ad-hoc (seeded cases were inserted by `harness seed`). Both
    # rows must exist before on_progress fires with run_id, since callers
    # (the task queue) reference it via a foreign key on first sight.
    seed.insert_case(case, adhoc=True)
    manifest = RunManifest(
        run_id=run_id,
        case_id=case.case_id,
        agent_model=agent_model,
        judge_model=judge_model,
        prompt_id=prompt_id,
        rubric_id=rubric.rubric_id,
        created_at=now_iso(),
        status="pending",
        sample_count=samples,
    )
    save_manifest(manifest, case_snapshot=case.to_dict())

    if on_progress:
        on_progress("prepare", 0, samples, run_id)

    # One context per run: backends (retriever) are shared across this run's
    # samples but isolated from concurrent runs.
    if context is None:
        context = RunContext()
    any_hard = False
    last_judgment_id = None
    for index in range(1, samples + 1):
        _, hard_failure, judgment = _execute_sample(
            case=case,
            prompt_text=prompt_text,
            prompt_id=prompt_id,
            rubric=rubric,
            run_id=run_id,
            sample_index=index,
            sample_total=samples,
            on_progress=on_progress,
            context=context,
        )
        any_hard = any_hard or hard_failure
        last_judgment_id = judgment.judgment_id
        if on_progress:
            on_progress("sample_done", index, samples, run_id)

    manifest.judgment_id = last_judgment_id
    manifest.hard_failure = any_hard
    manifest.status = "judged"
    save_manifest(manifest)
    return manifest


def run_case(
    case: Case,
    prompt_text: str,
    prompt_id: str,
    rubric: RubricVersion,
) -> RunManifest:
    return run_case_samples(case, prompt_text, prompt_id, rubric, samples=1)


def run_batch(
    cases: list[Case],
    prompt_text: str,
    prompt_id: str,
    rubric: RubricVersion,
) -> list[RunManifest]:
    return [run_case(case, prompt_text, prompt_id, rubric) for case in cases]
