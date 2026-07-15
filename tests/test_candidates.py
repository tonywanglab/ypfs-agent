from __future__ import annotations

import json

import pytest

from harness import candidates, llm, registry, reviews
from harness.models import Case, PromptVersion, RunManifest
from harness.seed import seed_all
from harness.storage import atomic_write_json
import harness.runner as runner


def _seed_registry(evals_dir):
    seed_all()


def _write_minimal_run(run_id: str):
    case = Case(case_id="c1", prompt="q")
    manifest = RunManifest(
        run_id=run_id, case_id="c1", role="adhoc", model="m",
        prompt_id="prompt_v1", rubric_id="rubric_v1", created_at="t", status="judged",
    )
    d = runner.RUNS_DIR / run_id
    d.mkdir(parents=True, exist_ok=True)
    atomic_write_json(d / "manifest.json", manifest.to_dict())
    atomic_write_json(d / "case.json", case.to_dict())
    atomic_write_json(d / "answer.json", {"answer": "a"})
    atomic_write_json(d / "trace.json", {})
    atomic_write_json(d / "checks.json", [])
    atomic_write_json(d / "checklist.json", {"checklist_id": "chk", "items": []})
    atomic_write_json(d / "judgment.json", {
        "judgment_id": "j", "summary": "s", "failure_feedback": "f", "criteria": [],
    })


def _review_id(run_id: str, attribution: str) -> str:
    return reviews.create_review(
        run_id, verdict="unacceptable", primary_problem="p", failure_attribution=attribution,
    ).review_id


def _mock_rubric_llm(monkeypatch):
    def fake_chat_json(system, user, model):
        return {
            "rationale": "tighten case study rule",
            "criteria": [
                {"id": "case_study_support", "description": "cite case studies", "check_type": "llm"},
                {"id": "no_survey_citations", "description": "no surveys", "check_type": "deterministic",
                 "deterministic_check": "no_survey_citations"},
            ],
        }

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)


def _mock_prompt_llm(monkeypatch):
    def fake_chat_json(system, user, model):
        return {"rationale": "more options", "text": "# Revised prompt\nBe explicit about tradeoffs."}

    monkeypatch.setattr(llm, "chat_json", fake_chat_json)


def test_propose_and_approve_rubric(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)

    _write_minimal_run("run_rubric")
    proposal = candidates.propose_rubric([_review_id("run_rubric", "rubric_gap")], "model-x")
    assert proposal.status == "proposed"
    assert registry.locked_branch() == "rubric"

    frozen = candidates.approve_rubric(proposal.rubric_id)
    assert frozen.status == "frozen"
    assert frozen.rubric_id.startswith("rubric_v")
    assert registry.active_rubric_id() == frozen.rubric_id
    assert registry.locked_branch() is None


def test_propose_rubric_conflicting_cycle_raises(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)
    registry.lock_cycle("prompt")

    with pytest.raises(registry.CycleLockedError):
        candidates.propose_rubric(["rev1"], "model-x")


def test_deny_rubric_closes_cycle(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)
    _write_minimal_run("run_deny")
    proposal = candidates.propose_rubric([_review_id("run_deny", "rubric_gap")], "model-x")
    denied = candidates.deny_rubric(proposal.rubric_id)
    assert denied.status == "rejected"
    assert registry.locked_branch() is None


def test_approve_rubric_with_edited_criteria(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)
    _write_minimal_run("run_edit")
    proposal = candidates.propose_rubric([_review_id("run_edit", "rubric_gap")], "model-x")
    edited = json.dumps([
        {"id": "new_criterion", "description": "custom", "check_type": "llm", "weight": 2.0},
    ])
    frozen = candidates.approve_rubric(proposal.rubric_id, criteria_json=edited)
    assert len(frozen.criteria) == 1
    assert frozen.criteria[0].id == "new_criterion"


def test_approve_rubric_rejects_empty_criteria(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)
    proposal = candidates.propose_rubric([], "model-x")

    with pytest.raises(ValueError, match="at least one criterion"):
        candidates.approve_rubric(proposal.rubric_id, criteria_json="[]")

    assert registry.active_rubric_id() == "rubric_v1"
    assert candidates.load_proposal(proposal.rubric_id).status == "proposed"


def test_failed_rubric_activation_keeps_proposal_recoverable(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)
    proposal = candidates.propose_rubric([], "model-x")
    frozen_path = candidates.RUBRICS_DIR / f"rubric_v{proposal.version}.json"

    def fail_activation(_rubric_id):
        raise RuntimeError("simulated registry failure")

    monkeypatch.setattr(registry, "set_active_rubric", fail_activation)
    with pytest.raises(RuntimeError, match="simulated registry failure"):
        candidates.approve_rubric(proposal.rubric_id)

    assert registry.active_rubric_id() == "rubric_v1"
    assert candidates.load_proposal(proposal.rubric_id).status == "proposed"
    assert not frozen_path.exists()


def test_repeated_stale_rubric_denial_does_not_close_new_cycle(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_rubric_llm(monkeypatch)
    proposal = candidates.propose_rubric([], "model-x")
    candidates.deny_rubric(proposal.rubric_id)
    registry.lock_cycle("prompt")

    with pytest.raises(ValueError, match="not in proposed status"):
        candidates.deny_rubric(proposal.rubric_id)

    assert registry.locked_branch() == "prompt"


def test_propose_prompt_writes_candidate(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    _mock_prompt_llm(monkeypatch)

    _write_minimal_run("run_prompt")
    candidate = candidates.propose_prompt([_review_id("run_prompt", "agent_failure")], "model-x")
    assert candidate.status == "candidate"
    assert "Revised prompt" in candidate.text
    assert registry.locked_branch() == "prompt"
    loaded = candidates.load_prompt_version(candidate.prompt_id)
    assert loaded.prompt_id == candidate.prompt_id


def test_prompt_proposal_failure_releases_new_cycle(evals_dir, monkeypatch):
    _seed_registry(evals_dir)

    def fail_chat_json(*args, **kwargs):
        raise RuntimeError("simulated provider failure")

    monkeypatch.setattr(llm, "chat_json", fail_chat_json)
    with pytest.raises(RuntimeError, match="simulated provider failure"):
        candidates.propose_prompt([], "model-x")

    assert registry.locked_branch() is None


def test_prompt_proposal_rejects_null_text_and_releases_cycle(evals_dir, monkeypatch):
    _seed_registry(evals_dir)
    monkeypatch.setattr(
        llm,
        "chat_json",
        lambda *args, **kwargs: {"rationale": "invalid", "text": None},
    )

    with pytest.raises(ValueError, match="non-empty string"):
        candidates.propose_prompt([], "model-x")

    assert registry.locked_branch() is None
    assert candidates.list_prompt_candidates() == []


def test_load_prompt_version_finds_candidate(evals_dir):
    _seed_registry(evals_dir)
    cand = PromptVersion(
        prompt_id="prompt_v2_abc", version=2, status="candidate", text="cand",
        created_at="t", parent_prompt_id="prompt_v1",
    )
    candidates.CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(candidates.CANDIDATES_DIR / f"{cand.prompt_id}.json", cand.to_dict())
    assert candidates.load_prompt_version(cand.prompt_id).text == "cand"
