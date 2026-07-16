from harness.models import RubricCriterion
from harness.rubric_markdown import criteria_to_markdown, markdown_to_criteria


def test_criteria_markdown_roundtrip():
    criteria = [
        RubricCriterion("quality", "Write a **good** answer.", "llm", weight=1.0),
        RubricCriterion(
            "completed",
            "Finished cleanly.",
            "deterministic",
            weight=2.0,
            deterministic_check="completed_without_error",
        ),
    ]
    restored = markdown_to_criteria(criteria_to_markdown(criteria))
    assert restored == criteria


def test_markdown_to_criteria_rejects_empty():
    try:
        markdown_to_criteria("")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "empty" in str(exc).lower()
