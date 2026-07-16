"""Diff the current active rubric criteria against a proposed revision."""

from __future__ import annotations

from .models import RubricCriterion

_COMPARE_FIELDS = ("description", "check_type", "weight", "deterministic_check")


def _field_changes(before: RubricCriterion, after: RubricCriterion) -> list[dict]:
    changes = []
    for field in _COMPARE_FIELDS:
        old = getattr(before, field)
        new = getattr(after, field)
        if old != new:
            changes.append({"field": field, "old": old, "new": new})
    return changes


def diff_rubric_criteria(
    current: list[RubricCriterion],
    proposal: list[RubricCriterion],
) -> list[dict]:
    """Return ordered diff rows: removed, changed, added, unchanged."""
    current_by_id = {c.id: c for c in current}
    proposal_by_id = {c.id: c for c in proposal}
    order = list(dict.fromkeys([c.id for c in current] + [c.id for c in proposal]))

    rows: list[dict] = []
    for cid in order:
        before = current_by_id.get(cid)
        after = proposal_by_id.get(cid)
        if before and after:
            field_changes = _field_changes(before, after)
            rows.append({
                "change": "changed" if field_changes else "unchanged",
                "id": cid,
                "current": before,
                "proposal": after,
                "field_changes": field_changes,
            })
        elif after:
            rows.append({
                "change": "added",
                "id": cid,
                "current": None,
                "proposal": after,
                "field_changes": [],
            })
        else:
            rows.append({
                "change": "removed",
                "id": cid,
                "current": before,
                "proposal": None,
                "field_changes": [],
            })

    rank = {"removed": 0, "changed": 1, "added": 2, "unchanged": 3}
    rows.sort(key=lambda r: (rank[r["change"]], r["id"]))
    return rows
