"""GitHub-style grouped line diffs for prompt drafts."""

from __future__ import annotations

from difflib import SequenceMatcher


def build_line_diff(before: str, after: str, context: int = 3) -> list[dict]:
    old_lines = before.splitlines()
    new_lines = after.splitlines()
    matcher = SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    groups = []

    for opcodes in matcher.get_grouped_opcodes(context):
        rows = []
        for tag, old_start, old_end, new_start, new_end in opcodes:
            if tag == "equal":
                for offset, text in enumerate(old_lines[old_start:old_end]):
                    rows.append({
                        "kind": "context",
                        "old_number": old_start + offset + 1,
                        "new_number": new_start + offset + 1,
                        "text": text,
                    })
            if tag in ("replace", "delete"):
                for offset, text in enumerate(old_lines[old_start:old_end]):
                    rows.append({
                        "kind": "delete",
                        "old_number": old_start + offset + 1,
                        "new_number": None,
                        "text": text,
                    })
            if tag in ("replace", "insert"):
                for offset, text in enumerate(new_lines[new_start:new_end]):
                    rows.append({
                        "kind": "add",
                        "old_number": None,
                        "new_number": new_start + offset + 1,
                        "text": text,
                    })

        first = opcodes[0]
        last = opcodes[-1]
        old_start, old_end = first[1] + 1, last[2]
        new_start, new_end = first[3] + 1, last[4]
        groups.append({
            "old_start": old_start,
            "old_count": max(0, old_end - old_start + 1),
            "new_start": new_start,
            "new_count": max(0, new_end - new_start + 1),
            "rows": rows,
        })
    return groups
