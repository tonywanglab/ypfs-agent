"""Serialize rubric criteria to editable Markdown and parse it back."""

from __future__ import annotations

import re

from .models import RubricCriterion

_HEADER_RE = re.compile(r"^##\s+(\S+)\s*$")
_META_RE = re.compile(r"^(check_type|weight|deterministic_check):\s*(.*)$")


def criteria_to_markdown(criteria: list[RubricCriterion]) -> str:
    blocks: list[str] = []
    for criterion in criteria:
        lines = [
            f"## {criterion.id}",
            f"check_type: {criterion.check_type}",
            f"weight: {criterion.weight}",
        ]
        if criterion.deterministic_check:
            lines.append(f"deterministic_check: {criterion.deterministic_check}")
        lines.append("")
        lines.append(criterion.description.strip())
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks).rstrip() + ("\n" if blocks else "")


def markdown_to_criteria(text: str) -> list[RubricCriterion]:
    text = (text or "").strip()
    if not text:
        raise ValueError("Rubric markdown cannot be empty")

    criteria: list[RubricCriterion] = []
    current_id: str | None = None
    meta: dict[str, str] = {}
    description_lines: list[str] = []
    in_description = False

    def flush() -> None:
        nonlocal current_id, meta, description_lines, in_description
        if current_id is None:
            return
        check_type = meta.get("check_type", "llm")
        try:
            weight = float(meta.get("weight", "1.0"))
        except ValueError as exc:
            raise ValueError(f"Invalid weight for criterion {current_id!r}") from exc
        deterministic_check = meta.get("deterministic_check") or None
        if deterministic_check in ("", "null", "None"):
            deterministic_check = None
        description = "\n".join(description_lines).strip()
        criteria.append(RubricCriterion(
            id=current_id,
            description=description,
            check_type=check_type,  # type: ignore[arg-type]
            weight=weight,
            deterministic_check=deterministic_check,
        ))
        current_id = None
        meta = {}
        description_lines = []
        in_description = False

    for raw_line in text.splitlines():
        header = _HEADER_RE.match(raw_line)
        if header:
            flush()
            current_id = header.group(1)
            continue
        if current_id is None:
            if raw_line.strip():
                raise ValueError("Rubric markdown must start with a ## criterion_id heading")
            continue
        if not in_description:
            meta_match = _META_RE.match(raw_line.strip())
            if meta_match:
                meta[meta_match.group(1)] = meta_match.group(2).strip()
                continue
            if not raw_line.strip():
                in_description = True
                continue
            in_description = True
        description_lines.append(raw_line)

    flush()
    if not criteria:
        raise ValueError("No rubric criteria found in markdown")
    return criteria
