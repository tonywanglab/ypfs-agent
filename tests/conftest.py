"""Shared pytest fixtures for the harness test suite.

Every test that touches harness storage gets an isolated evals/ directory:
each module's *_PATH constants (computed from storage.EVALS_DIR at import
time) are monkeypatched directly, so tests never read or mutate the real
repo's evals/ and don't depend on import-order/reload tricks.
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def evals_dir(tmp_path, monkeypatch):
    """An isolated evals/ directory with every harness module's path
    constants repointed at it. Extend the patch list as new modules with
    their own *_PATH constants are added."""
    new_dir = tmp_path / "evals"
    new_dir.mkdir()

    import harness.storage as storage
    import harness.registry as registry
    import harness.seed as seed

    monkeypatch.setattr(storage, "EVALS_DIR", new_dir)
    monkeypatch.setattr(registry, "REGISTRY_PATH", new_dir / "registry.json")
    monkeypatch.setattr(seed, "CASES_PATH", new_dir / "cases.jsonl")
    monkeypatch.setattr(seed, "RUBRIC_V1_PATH", new_dir / "rubrics" / "rubric_v1.json")
    monkeypatch.setattr(seed, "PROMPT_V1_PATH", new_dir / "prompts" / "prompt_v1.json")

    try:
        import harness.runner as runner

        monkeypatch.setattr(runner, "RUNS_DIR", new_dir / "runs")
        monkeypatch.setattr(runner, "PROMOTIONS_DIR", new_dir / "promotions")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.candidates as candidates

        monkeypatch.setattr(candidates, "RUBRICS_DIR", new_dir / "rubrics")
        monkeypatch.setattr(candidates, "PROPOSALS_DIR", new_dir / "rubrics" / "proposals")
        monkeypatch.setattr(candidates, "PROMPTS_DIR", new_dir / "prompts")
        monkeypatch.setattr(candidates, "CANDIDATES_DIR", new_dir / "prompts" / "candidates")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.promote as promote

        monkeypatch.setattr(promote, "ARCHIVE_DIR", new_dir / "prompts" / "archive")
        monkeypatch.setattr(promote, "PROMPTS_DIR", new_dir / "prompts")
        monkeypatch.setattr(promote, "CANDIDATES_DIR", new_dir / "prompts" / "candidates")
        monkeypatch.setattr(promote, "SYSTEM_PROMPT_PATH", tmp_path / "system_prompt.md")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.reviews as reviews

        monkeypatch.setattr(reviews, "REVIEWS_DIR", new_dir / "reviews")
    except (ImportError, AttributeError):
        pass

    yield new_dir
