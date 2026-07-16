from harness.text_diff import build_line_diff


def test_line_diff_groups_additions_deletions_and_context():
    groups = build_line_diff("one\nold\nthree", "one\nnew\nthree")
    rows = groups[0]["rows"]
    assert [(row["kind"], row["text"]) for row in rows] == [
        ("context", "one"),
        ("delete", "old"),
        ("add", "new"),
        ("context", "three"),
    ]
    assert rows[1]["old_number"] == 2
    assert rows[1]["new_number"] is None
    assert rows[2]["old_number"] is None
    assert rows[2]["new_number"] == 2


def test_identical_text_has_no_diff_groups():
    assert build_line_diff("same", "same") == []
