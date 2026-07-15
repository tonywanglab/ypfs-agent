from __future__ import annotations

import pytest

from harness import candidates, promote, registry
from harness.models import ABPair, Case, PromptVersion, RunManifest
from harness.runner import (
    load_promotion,
    promotion_has_blocked_candidate_run,
)
import harness.runner as runner
from harness.seed import seed_all
from harness.storage import atomic_write_json


def _write_run(run_id: str, *, role: str, blocked: bool, case_id: str = "c1"):
    case = Case(case_id=case_id, prompt="q")
    manifest = RunManifest(
        run_id=run_id, case_id=case_id, role=role, model="m",
        prompt_id="prompt_v1", rubric_id="rubric_v1", created_at="t",
        promotion_blocked=blocked, status="judged",
    )
    d = runner.RUNS_DIR / run_id
    d.mkdir(parents=True, exist_ok=True)
    atomic_write_json(d / "manifest.json", manifest.to_dict())
    atomic_write_json(d / "case.json", case.to_dict())
    atomic_write_json(d / "answer.json", {"answer": "a"})
    atomic_write_json(d / "trace.json", {})
    atomic_write_json(d / "checks.json", [])
    atomic_write_json(d / "checklist.json", {"checklist_id": "chk", "items": []})
    atomic_write_json(d / "judgment.json", {"judgment_id": "j", "criteria": []})


def _seed_promotion(evals_dir, *, blocked: bool = False):
    seed_all()
    registry.lock_cycle("prompt")
    cycle_id = registry.load()["cycle"]["cycle_id"]
    cand = PromptVersion(
        prompt_id="prompt_v2_test", version=2, status="candidate",
        text="# New active prompt\nUpdated.", created_at="t", parent_prompt_id="prompt_v1",
        cycle_id=cycle_id,
    )
    candidates.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(candidates.CANDIDATES_DIR / f"{cand.prompt_id}.json", cand.to_dict())

    promo_id = "promo_test"
    promo_dir = runner.PROMOTIONS_DIR / promo_id
    promo_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(promo_dir / "manifest.json", {
        "promotion_id": promo_id, "rubric_id": "rubric_v1",
        "incumbent_prompt_id": "prompt_v1", "candidate_prompt_id": cand.prompt_id,
        "case_ids": ["c1"], "created_at": "t", "status": "pending",
        "cycle_id": cycle_id,
    })
    _write_run("run_inc", role="incumbent", blocked=False)
    _write_run("run_cand", role="candidate", blocked=blocked)
    runner.append_jsonl(promo_dir / "pairs.jsonl", ABPair(
        case_id="c1", incumbent_run_id="run_inc", candidate_run_id="run_cand",
    ).to_dict())
    return promo_id, cand.prompt_id


def test_promotion_blocked_when_candidate_hard_failure(evals_dir):
    promo_id, _ = _seed_promotion(evals_dir, blocked=True)
    assert promotion_has_blocked_candidate_run(promo_id) is True


def test_promote_prompt_updates_registry_and_system_file(evals_dir, tmp_path):
    promo_id, cand_id = _seed_promotion(evals_dir, blocked=False)
    active = promote.promote_prompt(promo_id, cand_id)

    assert active.status == "active"
    assert registry.active_prompt_id() == cand_id
    assert registry.locked_branch() is None
    assert promote.SYSTEM_PROMPT_PATH.read_text() == "# New active prompt\nUpdated."

    promotion = load_promotion(promo_id)
    assert promotion.status == "approved"


def test_promote_prompt_raises_when_blocked(evals_dir):
    promo_id, cand_id = _seed_promotion(evals_dir, blocked=True)
    with pytest.raises(ValueError, match="hard failure"):
        promote.promote_prompt(promo_id, cand_id)


def test_deny_promotion_closes_cycle(evals_dir):
    promo_id, cand_id = _seed_promotion(evals_dir, blocked=False)
    promote.deny_promotion(promo_id, rationale="not ready")
    assert registry.locked_branch() is None
    assert load_promotion(promo_id).status == "denied"


def test_repeated_denial_does_not_close_another_cycle(evals_dir):
    promo_id, _ = _seed_promotion(evals_dir, blocked=False)
    promote.deny_promotion(promo_id, rationale="not ready")
    registry.lock_cycle("rubric")

    with pytest.raises(ValueError, match="not pending"):
        promote.deny_promotion(promo_id)

    assert registry.locked_branch() == "rubric"
    assert load_promotion(promo_id).status == "denied"


def test_stale_promotion_does_not_close_new_prompt_cycle(evals_dir):
    promo_id, _ = _seed_promotion(evals_dir, blocked=False)
    registry.close_cycle("cancelled", expected_branch="prompt")
    registry.lock_cycle("prompt", opened_by="new-cycle")

    with pytest.raises(ValueError, match="different review cycle"):
        promote.deny_promotion(promo_id)

    assert registry.locked_branch() == "prompt"
    assert load_promotion(promo_id).status == "pending"


def test_failed_promotion_rolls_back_all_artifacts(evals_dir, tmp_path, monkeypatch):
    promo_id, cand_id = _seed_promotion(evals_dir, blocked=False)
    blocked_system_path = tmp_path / "system-prompt-directory"
    blocked_system_path.mkdir()
    monkeypatch.setattr(promote, "SYSTEM_PROMPT_PATH", blocked_system_path)

    with pytest.raises(IsADirectoryError):
        promote.promote_prompt(promo_id, cand_id)

    assert registry.active_prompt_id() == "prompt_v1"
    assert registry.locked_branch() == "prompt"
    assert load_promotion(promo_id).status == "pending"
    assert candidates.load_prompt_version(cand_id).status == "candidate"
    assert not (promote.PROMPTS_DIR / f"{cand_id}.json").exists()
    assert not (promote.ARCHIVE_DIR / "prompt_v1.json").exists()
