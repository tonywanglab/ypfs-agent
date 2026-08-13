"""Seed cases and the immutable prompt version-one baseline (Postgres)."""

from __future__ import annotations

from . import dbio
from .models import Case, PromptVersion
from .storage import REPO_ROOT, now_iso

SYSTEM_PROMPT_PATH = REPO_ROOT / "agent" / "system_prompt.md"

SEED_CASES = [
    Case(
        case_id="broad_based_emergency_lending",
        prompt=(
            "I work for a central bank in a large developed economy. A globally "
            "significant bank headquartered in my country is experiencing a bank run, "
            "and there are signs that this trouble is spreading to other banks. I have "
            "been asked by my supervisor provide options for an emergency lending "
            "program that would be broadly available to all banks and would be a "
            "supplement to the standing facilities that already exist."
        ),
        tags=["plan", "bank_run"],
    ),
    Case(
        case_id="insurer_liquidity_plan",
        prompt=(
            "A natural disaster caused large losses at a globally significant insurance "
            "company in your jurisdiction. The credit rating of this company has been "
            "downgraded, investors are fleeing, and it is facing a short-term liquidity "
            "crisis. The company has asked the government for help. What do you "
            "recommend?"
        ),
        tags=["plan", "insurance"],
    ),
    Case(
        case_id="private_debt_fund_contagion",
        prompt=(
            "A large private-debt fund has just incurred a major loss, and the investors "
            "in this fund are facing significant write-downs on their positions. You have "
            "just learned that two large regional banks in your jurisdiction have made "
            "large commitments to this fund, and now have solvency concerns of their own. "
            "Investors and depositors are now worried about exposures at other regional "
            "banks, and since the exact pattern of exposures is unknown, the whole sector "
            "is facing runs. What, if anything, should the government do?"
        ),
        tags=["plan", "contagion"],
    ),
    Case(
        case_id="ai_collateral_shock",
        prompt=(
            "A Chinese company has just announced that it has achieved recursive "
            "self-improvement of a frontier LLM, without using Nvidia chips. This causes "
            "the equity prices of U.S. AI companies to crash, and the collateral used to "
            "back AI-company loans to fall significantly. This causes solvency concerns "
            "at several financial intermediaries, with a liquidity crisis feared to come. "
            "What should the government do?"
        ),
        tags=["plan", "systemic"],
    ),
]

def _case_from_row(row: dict) -> Case:
    return Case(
        case_id=row["case_id"],
        prompt=row["prompt"],
        tags=row["tags"] or [],
        notes=row["notes"] or "",
    )


def load_cases() -> list[Case]:
    """Seeded (non-adhoc) cases, for the case pickers."""
    rows = dbio.q("SELECT * FROM cases WHERE NOT adhoc ORDER BY case_id")
    return [_case_from_row(row) for row in rows]


def insert_case(case: Case, adhoc: bool = False) -> Case:
    """Insert a case if its id is new; existing rows are left untouched."""
    dbio.execute(
        """
        INSERT INTO cases (case_id, prompt, tags, notes, adhoc, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (case_id) DO NOTHING
        """,
        (case.case_id, case.prompt, dbio.jsonb(case.tags), case.notes, adhoc, now_iso()),
    )
    return case


def load_case(case_id: str) -> Case:
    row = dbio.q1("SELECT * FROM cases WHERE case_id = %s", (case_id,))
    if row is None:
        raise FileNotFoundError(f"Case {case_id!r} does not exist")
    return _case_from_row(row)


def seed_cases() -> list[Case]:
    for case in SEED_CASES:
        insert_case(case)
    return load_cases()


def seed_prompt_v1() -> PromptVersion:
    prompt = PromptVersion(
        prompt_id="prompt_v1",
        version=1,
        text=SYSTEM_PROMPT_PATH.read_text(),
        created_at=now_iso(),
        rationale="Seeded from the current agent/system_prompt.md.",
    )
    dbio.execute(
        """
        INSERT INTO prompt_versions (prompt_id, version, text, created_at,
                                     parent_prompt_id, rationale)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (prompt_id) DO NOTHING
        """,
        (prompt.prompt_id, prompt.version, prompt.text, prompt.created_at,
         prompt.parent_prompt_id, prompt.rationale),
    )
    from . import versions
    return versions.load_prompt("prompt_v1")


def seed_all() -> None:
    seed_cases()
    seed_prompt_v1()


if __name__ == "__main__":
    seed_all()
    print(f"Seeded {len(load_cases())} cases, prompt_v1 into Postgres")
