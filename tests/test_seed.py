from __future__ import annotations

from harness import seed


EXPECTED_CASE_IDS = {
    "broad_based_emergency_lending",
    "insurer_liquidity_plan",
    "private_debt_fund_contagion",
    "ai_collateral_shock",
}


def test_seed_cases_creates_expected_set(evals_dir):
    cases = seed.seed_cases()
    assert {c.case_id for c in cases} == EXPECTED_CASE_IDS
    assert seed.CASES_PATH.exists()


def test_seed_cases_is_idempotent(evals_dir):
    seed.seed_cases()
    first = seed.load_cases()
    seed.seed_cases()
    second = seed.load_cases()
    assert first == second


def test_seed_rubric_v1_is_frozen_with_deterministic_and_llm_criteria(evals_dir):
    rubric = seed.seed_rubric_v1()
    assert rubric.rubric_id == "rubric_v1"
    assert rubric.status == "frozen"
    det = [c for c in rubric.criteria if c.check_type == "deterministic"]
    llm = [c for c in rubric.criteria if c.check_type == "llm"]
    assert det and llm
    assert all(c.deterministic_check for c in det)
    assert all(c.deterministic_check is None for c in llm)


def test_seed_rubric_v1_is_idempotent(evals_dir):
    first = seed.seed_rubric_v1()
    second = seed.seed_rubric_v1()
    assert first == second


def test_seed_prompt_v1_mirrors_system_prompt(evals_dir):
    prompt = seed.seed_prompt_v1()
    assert prompt.prompt_id == "prompt_v1"
    assert prompt.status == "active"
    assert prompt.text == seed.SYSTEM_PROMPT_PATH.read_text()


def test_seed_prompt_v1_is_idempotent(evals_dir):
    first = seed.seed_prompt_v1()
    second = seed.seed_prompt_v1()
    assert first == second


def test_seed_all_is_idempotent_and_creates_registry(evals_dir):
    seed.seed_all()
    seed.seed_all()
    assert len(seed.load_cases()) == 4
    assert seed.RUBRIC_V1_PATH.exists()
    assert seed.PROMPT_V1_PATH.exists()

    from harness import registry

    assert registry.REGISTRY_PATH.exists()
