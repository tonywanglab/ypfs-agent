from __future__ import annotations

from harness import seed


EXPECTED_CASE_IDS = {
    "broad_based_emergency_lending",
    "insurer_liquidity_plan",
    "private_debt_fund_contagion",
    "ai_collateral_shock",
}


def test_seed_cases_creates_expected_set(pg):
    cases = seed.seed_cases()
    assert {c.case_id for c in cases} == EXPECTED_CASE_IDS


def test_seed_cases_is_idempotent(pg):
    seed.seed_cases()
    first = seed.load_cases()
    seed.seed_cases()
    second = seed.load_cases()
    assert first == second


def test_seed_cases_marks_rows_non_adhoc(pg):
    seed.seed_cases()
    from harness.seed import insert_case
    from harness.models import Case

    insert_case(Case(case_id="chat_adhoc_1", prompt="q"), adhoc=True)
    assert "chat_adhoc_1" not in {c.case_id for c in seed.load_cases()}
    assert seed.load_case("chat_adhoc_1").case_id == "chat_adhoc_1"


def test_seed_prompt_v1_mirrors_system_prompt(pg):
    prompt = seed.seed_prompt_v1()
    assert prompt.prompt_id == "prompt_v1"
    assert prompt.text == seed.SYSTEM_PROMPT_PATH.read_text()


def test_seed_prompt_v1_is_idempotent(pg):
    first = seed.seed_prompt_v1()
    second = seed.seed_prompt_v1()
    assert first == second


def test_seed_all_is_idempotent(pg):
    seed.seed_all()
    seed.seed_all()
    assert len(seed.load_cases()) == 4
