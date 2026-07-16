"""Split markdown into header-delimited sections.

Adapted from `chunk_documents.parse_sections` (repo root). Copied rather than
imported so this server stays self-contained and avoids chunk_documents.py's
module-load `tiktoken.encoding_for_model("gpt-4o")` — lexical search needs no
token counts, only the header split and the section-path breadcrumb.
"""

import re

HEADER_RE = re.compile(r"^(#{1,6})\s+(.+)$")
PAGE_RE = re.compile(r"^--- end of page(?:\.page_number)?=(\d+) ---\s*$")


def parse_sections(md_text: str) -> list[dict]:
    """Split markdown into sections at every header boundary.

    Returns a list of dicts, each with: header_text, header_level, body, page,
    section_path. section_path is the list of active header texts (ancestor +
    self) at the point this section starts, used as a breadcrumb.
    """
    lines = md_text.splitlines()
    sections: list[dict] = []
    current = None
    current_page = 1
    active_headers: dict[int, str] = {}  # level -> text, tracks doc hierarchy

    for line in lines:
        page_m = PAGE_RE.match(line)
        if page_m:
            current_page = int(page_m.group(1)) + 1
            continue

        header_m = HEADER_RE.match(line)
        if header_m:
            # Flush the in-progress section before starting the new one, so
            # active_headers still reflects the OLD section's context.
            if current is not None:
                body = "\n".join(current["body_lines"]).strip()
                if body:  # skip sections that are just a header with no body
                    path = [active_headers[lvl] for lvl in sorted(active_headers)]
                    sections.append({**current, "body": body, "section_path": path})

            level = len(header_m.group(1))
            # Strip bold markers pymupdf4llm sometimes wraps around header text
            header_text = re.sub(r"\*+", "", header_m.group(2)).strip()

            # Update breadcrumb: set this level's header, clear all deeper levels
            active_headers[level] = header_text
            for lvl in [k for k in active_headers if k > level]:
                del active_headers[lvl]

            current = {
                "header_text": header_text,
                "header_level": level,
                "body_lines": [],
                "page": current_page,
            }
        elif current is not None:
            current["body_lines"].append(line)

    # Flush the final section
    if current is not None:
        body = "\n".join(current["body_lines"]).strip()
        if body:
            path = [active_headers[lvl] for lvl in sorted(active_headers)]
            sections.append({**current, "body": body, "section_path": path})

    return sections
