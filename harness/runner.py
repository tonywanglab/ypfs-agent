"""Run the fixed agent, deterministic checks, and direct fixed judge."""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from agent.agent import run as agent_run

from . import config, evaluator
from .checks import any_hard_failure, run_checks
from .models import Case, RunManifest, Rubric
from .storage import EVALS_DIR, atomic_write_json, new_id, now_iso, read_json
from .trace import build_trace

RUNS_DIR = EVALS_DIR / "runs"
RunPhase = Literal["prepare", "agent", "checks", "judge", "sample_done"]
ProgressCallback = Callable[[RunPhase, int, int, str], None]


def _run_dir(run_id: str) -> Path:
    return RUNS_DIR / run_id


def _sample_dir(run_id: str, index: int) -> Path:
    return _run_dir(run_id) / "samples" / f"{index:02d}"


def _legacy_layout(run_dir: Path) -> bool:
    return (run_dir / "answer.json").exists() and not (run_dir / "samples").exists()


def _load_sample_artifacts(directory: Path) -> dict:
    checks = read_json(directory / "checks.json")
    return {
        "answer": read_json(directory / "answer.json")["answer"],
        "trace": read_json(directory / "trace.json"),
        "checks": checks,
        "judgment": read_json(directory / "judgment.json"),
        "hard_failure": any_hard_failure_from_dicts(checks),
    }


def any_hard_failure_from_dicts(checks: list[dict]) -> bool:
    return any(c.get("hard_failure") and not c.get("passed") for c in checks)


def save_manifest(manifest: RunManifest) -> None:
    atomic_write_json(_run_dir(manifest.run_id) / "manifest.json", manifest.to_dict())


def load_manifest(run_id: str) -> RunManifest:
    return RunManifest.from_dict(read_json(_run_dir(run_id) / "manifest.json"))


def load_run_bundle(run_id: str) -> dict:
    directory = _run_dir(run_id)
    manifest = read_json(directory / "manifest.json")
    case = read_json(directory / "case.json")
    samples: list[dict] = []

    if _legacy_layout(directory):
        artifacts = _load_sample_artifacts(directory)
        samples.append({"index": 1, **artifacts})
    else:
        samples_root = directory / "samples"
        if not samples_root.exists():
            raise FileNotFoundError(f"Run {run_id!r} has no sample artifacts")
        for sample_path in sorted(samples_root.iterdir()):
            if not sample_path.is_dir():
                continue
            try:
                index = int(sample_path.name)
            except ValueError:
                continue
            samples.append({"index": index, **_load_sample_artifacts(sample_path)})

    if not samples:
        raise FileNotFoundError(f"Run {run_id!r} has no sample artifacts")

    first = samples[0]
    return {
        "manifest": manifest,
        "case": case,
        "samples": samples,
        "answer": first["answer"],
        "trace": first["trace"],
        "checks": first["checks"],
        "judgment": first["judgment"],
    }


def list_runs() -> list[RunManifest]:
    if not RUNS_DIR.exists():
        return []
    manifests = []
    for directory in sorted(RUNS_DIR.iterdir()):
        manifest_path = directory / "manifest.json"
        if manifest_path.exists():
            manifests.append(RunManifest.from_dict(read_json(manifest_path)))
    return manifests


def delete_run(run_id: str) -> None:
    run_dir = _run_dir(run_id)
    if not (run_dir / "manifest.json").exists():
        raise FileNotFoundError(f"Run {run_id!r} does not exist")
    shutil.rmtree(run_dir)


def _execute_sample(
    *,
    case: Case,
    prompt_text: str,
    prompt_id: str,
    rubric: Rubric,
    run_id: str,
    sample_dir: Path,
    sample_index: int,
    sample_total: int,
    on_progress: ProgressCallback | None = None,
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
    sample_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(sample_dir / "answer.json", {"answer": answer})
    atomic_write_json(sample_dir / "trace.json", build_trace(messages, answer))
    atomic_write_json(
        sample_dir / "checks.json",
        [result.to_dict() for result in check_results],
    )
    atomic_write_json(sample_dir / "judgment.json", judgment.to_dict())
    hard_failure = any_hard_failure(check_results)
    return check_results, hard_failure, judgment


def run_case_samples(
    case: Case,
    prompt_text: str,
    prompt_id: str,
    rubric: Rubric,
    samples: int = 1,
    on_progress: ProgressCallback | None = None,
) -> RunManifest:
    samples = max(1, min(samples, 20))
    run_id = new_id("run")
    agent_model = config.agent_model()
    judge_model = config.judge_model()
    run_dir = _run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    if on_progress:
        on_progress("prepare", 0, samples, run_id)
    atomic_write_json(run_dir / "case.json", case.to_dict())

    any_hard = False
    last_judgment_id = None
    for index in range(1, samples + 1):
        _, hard_failure, judgment = _execute_sample(
            case=case,
            prompt_text=prompt_text,
            prompt_id=prompt_id,
            rubric=rubric,
            run_id=run_id,
            sample_dir=_sample_dir(run_id, index),
            sample_index=index,
            sample_total=samples,
            on_progress=on_progress,
        )
        any_hard = any_hard or hard_failure
        last_judgment_id = judgment.judgment_id
        if on_progress:
            on_progress("sample_done", index, samples, run_id)

    manifest = RunManifest(
        run_id=run_id,
        case_id=case.case_id,
        agent_model=agent_model,
        judge_model=judge_model,
        prompt_id=prompt_id,
        rubric_id=rubric.rubric_id,
        judgment_id=last_judgment_id,
        created_at=now_iso(),
        hard_failure=any_hard,
        status="judged",
        sample_count=samples,
    )
    save_manifest(manifest)
    return manifest


def run_case(
    case: Case,
    prompt_text: str,
    prompt_id: str,
    rubric: Rubric,
) -> RunManifest:
    return run_case_samples(case, prompt_text, prompt_id, rubric, samples=1)


def run_batch(
    cases: list[Case],
    prompt_text: str,
    prompt_id: str,
    rubric: Rubric,
) -> list[RunManifest]:
    return [run_case(case, prompt_text, prompt_id, rubric) for case in cases]
