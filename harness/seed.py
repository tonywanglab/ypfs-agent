"""Seed cases and immutable prompt/rubric version-one baselines (Postgres)."""

from __future__ import annotations

from . import dbio
from .models import Case, PromptVersion, RubricVersion, RubricCriterion
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

SEED_RUBRIC_CRITERIA = [
    RubricCriterion(
        id="survey_shapes_reasoning",
        description=(
            "Uses survey documents to shape the overarching analytical framing and plan "
            "structure."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="case_study_support",
        description=(
            "When making design suggestions, cites case studies similar to the user's "
            "problem and relevant to any surveys retrieved, rather than citing surveys "
            "directly."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="no_survey_citations",
        description="Never cites a document whose document_type is 'survey'.",
        check_type="deterministic",
        deterministic_check="no_survey_citations",
    ),
    RubricCriterion(
        id="citations_resolve",
        description=(
            "Every cited doc_id resolves to real corpus metadata and was actually "
            "retrieved or fetched during the run."
        ),
        check_type="deterministic",
        deterministic_check="citations_resolve",
    ),
    RubricCriterion(
        id="completed_without_error",
        description=(
            "The run produced a substantive final answer without a tool error or hitting "
            "the step limit."
        ),
        check_type="deterministic",
        deterministic_check="completed_without_error",
    ),
    RubricCriterion(
        id="options_structure",
        description=(
            "When asked for a plan or recommendation, presents multiple named "
            "options/archetypes with tradeoffs rather than a single prescriptive answer."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="advisory_stance",
        description=(
            "Illuminates options and tradeoffs for the principal to decide, rather than "
            "issuing an unqualified directive."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="bagehot_modernized",
        description=(
            "Treats Bagehot's dictum accurately ('lend freely, against good collateral, "
            "at a high rate') and does not treat 'lend only to solvent institutions' as "
            "canonical Bagehot doctrine."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="terminology_discipline",
        description=(
            "Handles loaded crisis terminology such as solvency, liquidity, and moral "
            "hazard with skepticism and precision rather than using labels as conclusions."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="viability_framing",
        description=(
            "Reframes solvency questions around whether creditors and markets believe "
            "the institution can continue as a going concern."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="moral_hazard_placement",
        description=(
            "When moral hazard is relevant, locates mitigation primarily in follow-on "
            "structural interventions rather than punitive emergency-loan conditions."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="stigma_and_penalty_pricing",
        description=(
            "Analyzes how punitive pricing and stigma can deter emergency borrowing and "
            "undermine a targeted intervention."
        ),
        check_type="llm",
    ),
    RubricCriterion(
        id="precedent_coverage",
        description=(
            "Retrieves and cites the most relevant historical case-study precedents in "
            "the corpus for the design question."
        ),
        check_type="llm",
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


def seed_rubric_v1() -> RubricVersion:
    rubric = RubricVersion(
        rubric_id="rubric_v1",
        version=1,
        criteria=SEED_RUBRIC_CRITERIA,
        created_at=now_iso(),
        rationale="Seeded from agent/system_prompt.md source-hierarchy and output-format policy.",
    )
    dbio.execute(
        """
        INSERT INTO rubric_versions (rubric_id, version, criteria, created_at,
                                     parent_rubric_id, rationale)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (rubric_id) DO NOTHING
        """,
        (rubric.rubric_id, rubric.version,
         dbio.jsonb([c.to_dict() for c in rubric.criteria]),
         rubric.created_at, rubric.parent_rubric_id, rubric.rationale),
    )
    from . import versions
    return versions.load_rubric("rubric_v1")


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
    seed_rubric_v1()
    seed_prompt_v1()


if __name__ == "__main__":
    seed_all()
    print(f"Seeded {len(load_cases())} cases, rubric_v1, prompt_v1 into Postgres")
