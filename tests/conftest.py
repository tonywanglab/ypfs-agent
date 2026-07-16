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
    import harness.seed as seed

    monkeypatch.setattr(storage, "EVALS_DIR", new_dir)
    monkeypatch.setattr(seed, "CASES_PATH", new_dir / "cases.jsonl")
    monkeypatch.setattr(seed, "RUBRIC_V1_PATH", new_dir / "rubrics" / "rubric_v1.json")
    monkeypatch.setattr(seed, "PROMPT_V1_PATH", new_dir / "prompts" / "prompt_v1.json")

    try:
        import harness.runner as runner

        monkeypatch.setattr(runner, "RUNS_DIR", new_dir / "runs")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.versions as versions

        monkeypatch.setattr(versions, "RUBRICS_DIR", new_dir / "rubrics")
        monkeypatch.setattr(versions, "PROMPTS_DIR", new_dir / "prompts")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.reviews as reviews

        monkeypatch.setattr(reviews, "REVIEWS_DIR", new_dir / "reviews")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.jobs as jobs_mod

        monkeypatch.setattr(jobs_mod, "JOBS_DIR", new_dir / "jobs")
    except (ImportError, AttributeError):
        pass

    try:
        import harness.web as web

        monkeypatch.setattr(web, "EVALS_DIR", new_dir)
    except (ImportError, AttributeError):
        pass

    yield new_dir
