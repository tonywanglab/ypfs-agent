"""Sample OCR / image-extraction quality across converted docs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from figure_filters import is_junk_image

MARKDOWN_DIR = Path("markdown")
ASSETS_DIR = Path("assets")

PICTURE_TEXT = re.compile(r"Start of picture text")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def audit_doc(doc_id: str) -> dict:
    md_path = MARKDOWN_DIR / f"{doc_id}.md"
    if not md_path.exists():
        return {"doc_id": doc_id, "missing": True}

    md = md_path.read_text(encoding="utf-8")
    assets = ASSETS_DIR / doc_id
    images_in_md = IMAGE_RE.findall(md)
    junk_files = []
    good_files = []

    for ref in images_in_md:
        name = Path(ref).name
        p = assets / name
        if p.exists():
            (junk_files if is_junk_image(p) else good_files).append(name)

    for p in assets.glob("*.png"):
        if p.name not in {Path(r).name for r in images_in_md}:
            if is_junk_image(p):
                junk_files.append(p.name + " (orphan)")

    return {
        "doc_id": doc_id,
        "picture_text_blocks": len(PICTURE_TEXT.findall(md)),
        "images_in_md": len(images_in_md),
        "junk_images": junk_files,
        "good_images": good_files,
        "figure_markers": md.count("[FIGURE "),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit OCR/image quality")
    parser.add_argument("--doc", action="append", help="doc id (repeatable)")
    parser.add_argument("--sample", type=int, default=0, help="audit first N markdown files")
    args = parser.parse_args()

    if args.doc:
        docs = args.doc
    elif args.sample:
        docs = sorted(p.stem for p in MARKDOWN_DIR.glob("*.md"))[: args.sample]
    else:
        docs = sorted(p.stem for p in MARKDOWN_DIR.glob("*.md"))

    total_junk = total_pt = 0
    for doc_id in docs:
        r = audit_doc(doc_id)
        if r.get("missing"):
            print(f"{doc_id}: no markdown")
            continue
        total_junk += len(r["junk_images"])
        total_pt += r["picture_text_blocks"]
        flags = []
        if r["junk_images"]:
            flags.append(f"junk={r['junk_images']}")
        if r["picture_text_blocks"]:
            flags.append(f"picture_text={r['picture_text_blocks']}")
        status = ", ".join(flags) if flags else "ok"
        print(
            f"{doc_id}: {status} | imgs={r['images_in_md']} "
            f"markers={r['figure_markers']}"
        )

    print(f"\n{len(docs)} docs | junk images: {total_junk} | picture-text blocks left: {total_pt}")


if __name__ == "__main__":
    main()
