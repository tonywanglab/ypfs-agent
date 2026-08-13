"""
Phase 1b: Post-process markdown/ → insert [FIGURE] markers (Option B hybrid).

Reads pymupdf4llm output, strips chart OCR junk, pairs captions with images,
writes annotated markdown with [FIGURE ...] lines. Renames images to figure_N.png.
Falls back to PyMuPDF image detection for uncaptioned exhibits.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from figure_filters import is_junk_image, purge_unreferenced_images

MARKDOWN_DIR = Path("markdown")
ASSETS_DIR = Path("assets")

KIND = r"(Figure|Fig\.|Table|Chart|Diagram|Exhibit)"
KIND_ALT = r"Figure|Fig\.|Table|Chart|Diagram|Exhibit"
NUM = r"(\d+[a-z]?)"
SEP = r"(?:\s*[:\.\-–—]\s*(.+))?"
APPENDIX = r"(?:Appendix\s+)?"

PICTURE_CAPTION_RE = re.compile(
    rf"^{APPENDIX}(?:{KIND_ALT})\s+(\d+[a-z]?)\s*[:\.\-–—]\s*(.*)$",
    re.I,
)

CAPTION_RE = re.compile(
    rf"^{APPENDIX}{KIND}\s+{NUM}{SEP}\s*$",
    re.I,
)
BOLD_CAPTION_RE = re.compile(
    rf"^\*{{2}}{APPENDIX}{KIND}\s+{NUM}{SEP}\*{{2}}\s*$",
    re.I,
)
HEADER_CAPTION_RE = re.compile(
    rf"^#{{1,6}}\s+\*{{0,2}}{APPENDIX}{KIND}\s+{NUM}{SEP}\*{{0,2}}\s*$",
    re.I,
)
NARRATIVE_RE = re.compile(
    rf"^{APPENDIX}(?:Figure|Fig\.)\s+\d+\s+(?:shows|plots|gives|and|links|reprints|highlights|visualizes|depicts)\b",
    re.I,
)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
PAGE_SEP_RE = re.compile(r"^--- end of page(?:\.page_number)?=(\d+) ---\s*$")
PICTURE_TEXT_START = re.compile(r"\*\*----- Start of picture text -----")
PICTURE_TEXT_END = re.compile(r"\*\*----- End of picture text -----")

CHART_CUES = re.compile(
    r"%|€|\$|billion|axis|rate|volume|index|spread|yield|percent",
    re.I,
)
DIAGRAM_CUES = re.compile(
    r"structure|flow|map|schematic|model|timeline|network",
    re.I,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+")
FIGURE_MARKER_RE = re.compile(r"^\[FIGURE\s")
DEFAULT_PARENT_HEADING_LEVEL = 2


def infer_type(label_kind: str, caption: str) -> str:
    kind = label_kind.lower().rstrip(".")
    if kind.startswith("table"):
        return "table"
    cap = caption or ""
    if DIAGRAM_CUES.search(cap):
        return "diagram"
    if CHART_CUES.search(cap):
        return "chart"
    return "figure"


def slugify_label(kind: str, num: str) -> str:
    base = kind.lower().replace("fig.", "figure").replace(" ", "_")
    base = re.sub(r"[^a-z0-9_]", "", base)
    if base.startswith("fig"):
        base = "figure"
    return f"{base}_{num}"


def normalize_kind(kind: str) -> str:
    k = kind.lower().rstrip(".")
    if k.startswith("fig"):
        return "Figure"
    return kind[0].upper() + kind[1:]


def make_label(kind: str, num: str, line: str) -> str:
    base = normalize_kind(kind)
    if re.search(r"\bAppendix\s+", line, re.I):
        return f"Appendix {base} {num}"
    return f"{base} {num}"


def heading_level(line: str) -> int | None:
    m = HEADING_RE.match(line.strip())
    return len(m.group(1)) if m else None


def is_section_heading(line: str) -> bool:
    level = heading_level(line)
    return level is not None and parse_caption_line(line) is None


def format_figure_heading(parent_level: int, label: str, caption: str = "") -> str:
    """Render figure caption one markdown heading level below the parent section."""
    depth = min(max(parent_level, 1) + 1, 6)
    prefix = "#" * depth
    if caption:
        return f"{prefix} **{label}: {caption}**"
    return f"{prefix} **{label}**"


def parse_caption_line(line: str) -> tuple[str, str, str, str] | None:
    """Return (kind, num, caption_text, label) if line is a standalone caption."""
    stripped = line.strip()
    if NARRATIVE_RE.match(stripped):
        return None

    for pat, needs_sep in (
        (HEADER_CAPTION_RE, False),
        (BOLD_CAPTION_RE, False),
        (CAPTION_RE, True),
    ):
        m = pat.match(stripped)
        if not m:
            continue
        kind, num, rest = m.group(1), m.group(2), m.group(3)
        if needs_sep and rest is None and not re.search(
            rf"{re.escape(num)}\s*[:\.\-–—]", stripped
        ):
            continue
        caption = (rest or "").strip().strip("*")
        label = make_label(kind, num, stripped)
        return kind, num, caption, label
    return None


def is_caption_line(line: str) -> re.Match | None:
    """Backward-compatible wrapper; returns a match-like object with .groups()."""
    parsed = parse_caption_line(line)
    if not parsed:
        return None
    kind, num, caption, _ = parsed

    class _Match:
        def groups(self):
            return kind, num, caption

    return _Match()


def collect_picture_text_block(lines: list[str], i: int) -> tuple[int, str]:
    """Return (index after block, raw block text)."""
    if i >= len(lines) or not PICTURE_TEXT_START.search(lines[i]):
        return i, ""
    parts = [lines[i]]
    if PICTURE_TEXT_END.search(lines[i]):
        return i + 1, "\n".join(parts)
    i += 1
    while i < len(lines):
        parts.append(lines[i])
        if PICTURE_TEXT_END.search(lines[i]):
            return i + 1, "\n".join(parts)
        i += 1
    return i, "\n".join(parts)


def skip_picture_text_block(lines: list[str], i: int) -> int:
    end, _ = collect_picture_text_block(lines, i)
    return end


def is_chart_junk_line(s: str) -> bool:
    if re.match(r"^(?:Note|Sources)\b", s, re.I):
        return True
    if re.match(r"^-?\d+\.?\d*$", s.strip()):
        return True
    if re.match(r"^Capital Raised\s*\(", s, re.I):
        return True
    if re.match(r"^Percentage of Capital", s, re.I):
        return True
    words = s.split()
    if len(words) > 8 and ":" not in s:
        return True
    if len(s) < 25 and not re.search(r"[,\(\)]", s):
        if re.search(r"\d", s) or s in ("Common Preferred Debt", "ban", "Debt"):
            return True
    return False


def rescue_caption_from_picture_text(raw: str) -> tuple[str, str, str, str] | None:
    """Extract Figure N: / Table N: caption embedded in pymupdf4llm OCR blocks."""
    text = PICTURE_TEXT_START.sub("", raw)
    text = PICTURE_TEXT_END.sub("", text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = text.replace("**", "")

    ocr_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not ocr_lines:
        return None

    for idx, ln in enumerate(ocr_lines):
        m = PICTURE_CAPTION_RE.match(ln)
        if not m:
            continue
        num, rest = m.group(1), m.group(2).strip()
        kind_m = re.match(rf"^{APPENDIX}({KIND_ALT})\s+", ln, re.I)
        kind = kind_m.group(1) if kind_m else "Figure"
        caption_parts = [rest] if rest else []
        for cont in ocr_lines[idx + 1 :]:
            if is_chart_junk_line(cont):
                break
            if PICTURE_CAPTION_RE.match(cont):
                break
            caption_parts.append(cont)

        caption = " ".join(caption_parts).strip()
        label = make_label(kind, num, ln)
        return kind, num, caption, label
    return None


def find_nearby_image_before(
    lines: list[str], idx: int, assets_base: Path, window: int = 5
) -> tuple[Path | None, int]:
    """Look backward for a markdown image (common before picture-text blocks)."""
    for j in range(idx - 1, max(-1, idx - window - 1), -1):
        if j < 0:
            break
        stripped = lines[j].strip()
        if not stripped or stripped.startswith("**==>"):
            continue
        img_m = IMAGE_RE.match(stripped)
        if img_m:
            img_src = resolve_image(Path(img_m.group(2)), assets_base)
            if img_src:
                return img_src, j
        if parse_caption_line(lines[j]) or PICTURE_TEXT_START.search(stripped):
            break
    return None, idx


def peek_picture_text_ahead(lines: list[str], idx: int, window: int = 6) -> tuple[int, str] | None:
    for j in range(idx + 1, min(len(lines), idx + window + 1)):
        stripped = lines[j].strip()
        if not stripped:
            continue
        if PICTURE_TEXT_START.search(stripped):
            end, raw = collect_picture_text_block(lines, j)
            return end, raw
        if IMAGE_RE.match(stripped) or parse_caption_line(lines[j]):
            break
    return None


def format_marker(
    doc_id: str,
    seq: int,
    fig_type: str,
    page: int | None,
    label: str,
    filename: str,
    caption: str,
) -> str:
    page_part = f" page={page}" if page is not None else ""
    cap = caption.replace('"', "'").strip()
    return (
        f'[FIGURE id={doc_id}_f{seq} type={fig_type}{page_part} '
        f'label="{label}" file={filename} caption="{cap}"]'
    )


def resolve_image(path: Path, assets_base: Path) -> Path | None:
    if not path.is_absolute():
        resolved = None
        for base in (assets_base, MARKDOWN_DIR):
            candidate = (base / path.name).resolve()
            if candidate.exists():
                resolved = candidate
                break
        if resolved is None:
            candidate = (MARKDOWN_DIR / path).resolve()
            resolved = candidate if candidate.exists() else None
        path = resolved
    if path is None or not path.exists() or is_junk_image(path):
        if path and path.exists() and is_junk_image(path):
            path.unlink(missing_ok=True)
        return None
    return path


def rename_asset(doc_id: str, src: Path, filename: str) -> Path:
    dest_dir = ASSETS_DIR / doc_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename
    if src.resolve() != dest.resolve():
        if dest.exists():
            dest.unlink()
        shutil.move(str(src), str(dest))
    return dest


def find_nearby_image(
    lines: list[str], idx: int, assets_base: Path
) -> tuple[Path | None, int]:
    """Look within ±3 lines for a markdown image."""
    for j in range(max(0, idx - 3), min(len(lines), idx + 4)):
        if j == idx:
            continue
        j = skip_picture_text_block(lines, j)
        if j >= len(lines):
            break
        img_m = IMAGE_RE.match(lines[j].strip())
        if img_m:
            img_src = resolve_image(Path(img_m.group(2)), assets_base)
            if img_src:
                return img_src, j
    return None, idx


def find_ahead_caption(
    lines: list[str], idx: int, window: int = 6
) -> tuple[str, str, str, str, int] | None:
    """Look ahead for a caption line (image-before-caption layout)."""
    j = idx + 1
    end = min(len(lines), idx + window + 1)
    while j < end:
        j = skip_picture_text_block(lines, j)
        if j >= len(lines):
            break
        stripped = lines[j].strip()
        if not stripped:
            j += 1
            continue
        parsed = parse_caption_line(lines[j])
        if parsed:
            kind, num, caption, label = parsed
            return kind, num, caption, label, j
        if IMAGE_RE.match(stripped):
            break
        j += 1
    return None


def emit_figure(
    out: list[str],
    doc_id: str,
    seq: int,
    kind: str,
    num: str,
    caption: str,
    label: str,
    current_page: int | None,
    img_src: Path | None,
) -> None:
    if img_src and is_junk_image(img_src):
        img_src.unlink(missing_ok=True)
        img_src = None
    fig_type = infer_type(kind, caption)
    filename = f"{slugify_label(kind, num)}.png"
    if img_src and img_src.exists():
        rename_asset(doc_id, img_src, filename)
    out.append(
        format_marker(doc_id, seq, fig_type, current_page, label, filename, caption)
    )
    if img_src and img_src.exists():
        out.append(f"![{label}](assets/{doc_id}/{filename})")


def annotate_markdown(doc_id: str, md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    seq = 0
    current_page: int | None = None
    parent_heading_level = DEFAULT_PARENT_HEADING_LEVEL
    i = 0
    assets_base = ASSETS_DIR / doc_id

    while i < len(lines):
        line = lines[i]
        page_m = PAGE_SEP_RE.match(line.strip())
        if page_m:
            current_page = int(page_m.group(1)) + 1
            i += 1
            continue

        if FIGURE_MARKER_RE.match(line.strip()):
            i += 1
            continue

        if is_section_heading(line):
            parent_heading_level = heading_level(line) or parent_heading_level

        if PICTURE_TEXT_START.search(line):
            end_i, block_raw = collect_picture_text_block(lines, i)
            rescued = rescue_caption_from_picture_text(block_raw)
            if rescued:
                kind, num, caption, label = rescued
                img_src, _ = find_nearby_image_before(lines, i, assets_base)
                seq += 1
                emit_figure(
                    out, doc_id, seq, kind, num, caption, label, current_page, img_src
                )
                out.append(format_figure_heading(parent_heading_level, label, caption))
            i = end_i
            continue

        line = lines[i]

        cap_m = is_caption_line(line)
        if cap_m:
            kind, num, rest = cap_m.groups()
            label = make_label(kind, num, line)
            caption = (rest or "").strip()
            fig_type = infer_type(kind, caption)
            filename = f"{slugify_label(kind, num)}.png"

            j = skip_picture_text_block(lines, i + 1)
            img_src, img_idx = find_nearby_image(lines, i, assets_base)
            if img_src:
                j = max(j, img_idx + 1)

            seq += 1
            out.append(
                format_marker(doc_id, seq, fig_type, current_page, label, filename, caption)
            )
            out.append(format_figure_heading(parent_heading_level, label, caption))
            if img_src and img_src.exists():
                rename_asset(doc_id, img_src, filename)
                out.append(f"![{label}](assets/{doc_id}/{filename})")
            i = j
            continue

        img_m = IMAGE_RE.match(line.strip())
        if img_m and (not out or not out[-1].startswith("[FIGURE")):
            img_src = resolve_image(Path(img_m.group(2)), assets_base)
            if not img_src:
                i += 1
                continue

            ahead_pt = peek_picture_text_ahead(lines, i)
            if ahead_pt:
                end_i, block_raw = ahead_pt
                rescued = rescue_caption_from_picture_text(block_raw)
                if rescued:
                    kind, num, caption, label = rescued
                    seq += 1
                    emit_figure(
                        out, doc_id, seq, kind, num, caption, label,
                        current_page, img_src,
                    )
                    out.append(format_figure_heading(parent_heading_level, label, caption))
                    i = end_i
                    continue

            ahead = find_ahead_caption(lines, i)
            seq += 1
            if ahead:
                kind, num, caption, label, cap_idx = ahead
                emit_figure(
                    out, doc_id, seq, kind, num, caption, label,
                    current_page, img_src,
                )
                out.append(format_figure_heading(parent_heading_level, label, caption))
                i = cap_idx + 1
                continue

            filename = f"exhibit_{seq}.png"
            rename_asset(doc_id, img_src, filename)
            out.append(
                format_marker(
                    doc_id, seq, "figure", current_page, f"Exhibit {seq}", filename, ""
                )
            )
            out.append(f"![Exhibit {seq}](assets/{doc_id}/{filename})")
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out).strip() + "\n"


def annotate_doc(doc_id: str, force: bool = False) -> bool:
    md_path = MARKDOWN_DIR / f"{doc_id}.md"
    if not md_path.exists():
        print(f"skipped {doc_id} — no markdown/{doc_id}.md (run pdf_to_markdown.py first)")
        return False

    text = md_path.read_text(encoding="utf-8")
    if "[FIGURE " in text and not force:
        return False

    annotated = annotate_markdown(doc_id, text)
    orphans = purge_unreferenced_images(annotated, doc_id, ASSETS_DIR)
    if orphans:
        print(f"  purged {orphans} orphan image(s) for {doc_id}")
    md_path.write_text(annotated, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Insert [FIGURE] markers into markdown/")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--doc", help="e.g. vol2_iss3_14")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.doc:
        docs = [args.doc]
    elif args.all:
        docs = [p.stem for p in sorted(MARKDOWN_DIR.glob("*.md"))]
    else:
        parser.print_help()
        return

    if not docs:
        sys.exit("No markdown files found. Run: python pdf_to_markdown.py --all")

    done = skipped = 0
    for doc_id in docs:
        if annotate_doc(doc_id, force=args.force):
            print(f"annotated {doc_id}")
            done += 1
        else:
            skipped += 1
    print(f"done: {done} annotated, {skipped} skipped")


if __name__ == "__main__":
    main()
