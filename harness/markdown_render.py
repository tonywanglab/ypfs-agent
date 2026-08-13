"""Render agent markdown answers for the harness UI."""

from __future__ import annotations

import markdown

_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


def render_markdown(text: str) -> str:
    if not text:
        return ""
    return markdown.markdown(text, extensions=_EXTENSIONS)
