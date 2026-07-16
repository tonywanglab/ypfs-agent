from __future__ import annotations

from harness.models import RubricCriterion
from harness.rubric_diff import diff_rubric_criteria


def test_diff_rubric_criteria_added_removed_changed():
    parent = [
        RubricCriterion(id="keep", description="same", check_type="llm"),
        RubricCriterion(id="drop", description="gone", check_type="llm"),
        RubricCriterion(
            id="edit", description="old text", check_type="deterministic",
            deterministic_check="completed_without_error",
        ),
    ]
    proposal = [
        RubricCriterion(id="keep", description="same", check_type="llm"),
        RubricCriterion(id="new_one", description="fresh", check_type="llm"),
        RubricCriterion(
            id="edit", description="new text", check_type="deterministic",
            deterministic_check="no_survey_citations",
        ),
    ]

    rows = {r["id"]: r for r in diff_rubric_criteria(parent, proposal)}

    assert rows["drop"]["change"] == "removed"
    assert rows["new_one"]["change"] == "added"
    assert rows["keep"]["change"] == "unchanged"
    assert rows["edit"]["change"] == "changed"
    assert len(rows["edit"]["field_changes"]) == 2
