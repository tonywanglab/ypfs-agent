"""Filter junk images and chart OCR blocks from pymupdf4llm output."""

from __future__ import annotations

import re
from pathlib import Path

import pymupdf

# Decorative rules, icon slivers, and OCR noise — not real figures.
MIN_FIGURE_WIDTH = 40
MIN_FIGURE_HEIGHT = 48
MIN_FIGURE_AREA = 10_000
MAX_ASPECT_RATIO = 10.0
# Full-width horizontal rules pymupdf4llm often emits (~800×40–70 px).
MAX_RULE_STRIP_HEIGHT = 75
MIN_RULE_STRIP_WIDTH = 280

PICTURE_TEXT_START = re.compile(r"\*\*----- Start of picture text -----")
PICTURE_TEXT_END = re.compile(r"\*\*----- End of picture text -----")
IMAGE_MD_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
FIGURE_FILE_RE = re.compile(r"\bfile=([^\s\]]+\.png)")


def is_horizontal_rule_strip(w: int, h: int) -> bool:
    """Wide, very short strips — page dividers / vector rules, not charts."""
    short = min(w, h)
    long = max(w, h)
    if short > MAX_RULE_STRIP_HEIGHT:
        return False
    if long < MIN_RULE_STRIP_WIDTH:
        return False
    return long / max(short, 1) >= 5.0


def is_junk_image(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        pix = pymupdf.Pixmap(str(path))
        w, h = pix.width, pix.height
    except Exception:
        return True
    area = w * h
    aspect = max(w, h) / max(min(w, h), 1)
    if h < MIN_FIGURE_HEIGHT or w < MIN_FIGURE_WIDTH:
        return True
    if area < MIN_FIGURE_AREA:
        return True
    if is_horizontal_rule_strip(w, h):
        return True
    if aspect > MAX_ASPECT_RATIO:
        return True
    return False


def strip_picture_text_blocks(md: str) -> str:
    """Remove pymupdf4llm chart OCR blocks (axis labels, garbled Tesseract output)."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if PICTURE_TEXT_START.search(lines[i]):
            if PICTURE_TEXT_END.search(lines[i]):
                i += 1
                continue
            i += 1
            while i < len(lines) and not PICTURE_TEXT_END.search(lines[i]):
                i += 1
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out).strip() + "\n"


def image_refs_in_markdown(md: str) -> set[str]:
    """Basenames of PNG files referenced in markdown or [FIGURE] markers."""
    names: set[str] = set()
    for _alt, ref in IMAGE_MD_RE.findall(md):
        names.add(Path(ref).name)
    for ref in FIGURE_FILE_RE.findall(md):
        names.add(Path(ref).name)
    return names


def resolve_asset_path(doc_id: str, ref: str, assets_dir: Path) -> Path | None:
    name = Path(ref).name
    for candidate in (
        assets_dir / doc_id / name,
        assets_dir / name,
        Path(ref),
    ):
        if candidate.exists():
            return candidate
    return None


def purge_unreferenced_images(md: str, doc_id: str, assets_dir: Path) -> int:
    """Delete PNGs on disk that are not referenced in markdown (extraction leftovers)."""
    doc_assets = assets_dir / doc_id
    if not doc_assets.is_dir():
        return 0
    keep = image_refs_in_markdown(md)
    removed = 0
    for png in doc_assets.glob("*.png"):
        if png.name not in keep:
            png.unlink(missing_ok=True)
            removed += 1
    return removed


def remove_junk_images(md: str, doc_id: str, assets_dir: Path) -> tuple[str, int]:
    """Drop markdown image refs for junk PNGs; optionally delete the files."""
    removed = 0
    lines = []
    for line in md.splitlines():
        m = IMAGE_MD_RE.match(line.strip())
        if m:
            rel = Path(m.group(2))
            candidates = [
                assets_dir / doc_id / rel.name,
                assets_dir / rel,
                Path(rel),
            ]
            img_path = next((p for p in candidates if p.exists()), None)
            if img_path and is_junk_image(img_path):
                img_path.unlink(missing_ok=True)
                removed += 1
                continue
        lines.append(line)
    return "\n".join(lines).strip() + "\n", removed


def clean_pymupdf4llm_markdown(md: str, doc_id: str, assets_dir: Path) -> tuple[str, int]:
    """Remove junk image refs and delete unreferenced PNG leftovers."""
    md, junk_removed = remove_junk_images(md, doc_id, assets_dir)
    orphan_removed = purge_unreferenced_images(md, doc_id, assets_dir)
    return md, junk_removed + orphan_removed
