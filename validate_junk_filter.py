"""
Validation run: convert + annotate a fixed doc set and assert no junk images
survive in markdown refs or [FIGURE] markers.

Exit 0 = pass, 1 = junk leaked or pipeline error.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import pymupdf

from figure_filters import is_junk_image

# Known rule-strip doc + pilot diversity + docs that previously leaked junk
VALIDATION_DOCS = [
    "vol1_iss1_1",   # horizontal rule artifact (999×66 strip)
    "vol3_iss2_13",  # 688×24 strip leaked into markdown
    "vol4_iss3_3",   # exhibit_1/2 were rule strips
    "vol1_iss3_7",
    "vol2_iss3_14",
    "vol4_iss2_1",
    "vol4_iss2_37",
    "vol1_iss4_10",  # text-only control
]

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
FIGURE_FILE_RE = re.compile(r"\bfile=([^\s\]]+\.png)")


def run_step(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr, sep="\n")
        raise SystemExit(f"failed: {' '.join(cmd)}")


def image_refs(md: str) -> list[str]:
    refs = IMAGE_RE.findall(md) + FIGURE_FILE_RE.findall(md)
    return list(dict.fromkeys(refs))


def resolve_asset(doc_id: str, ref: str) -> Path | None:
    name = Path(ref).name
    for candidate in (
        Path("assets") / doc_id / name,
        Path(ref),
        Path("assets") / doc_id / Path(ref).name,
    ):
        if candidate.exists():
            return candidate
    return None


def audit_doc(doc_id: str) -> dict:
    md_path = Path("markdown") / f"{doc_id}.md"
    md = md_path.read_text(encoding="utf-8")
    leaked: list[tuple[str, str, int, int]] = []
    kept: list[tuple[str, int, int]] = []

    for ref in image_refs(md):
        path = resolve_asset(doc_id, ref)
        if path is None:
            continue
        pix = pymupdf.Pixmap(str(path))
        w, h = pix.width, pix.height
        if is_junk_image(path):
            leaked.append((ref, path.name, w, h))
        else:
            kept.append((path.name, w, h))

    orphans = []
    asset_dir = Path("assets") / doc_id
    if asset_dir.exists():
        referenced = {Path(r).name for r in image_refs(md)}
        for p in asset_dir.glob("*.png"):
            if p.name not in referenced and not is_junk_image(p):
                orphans.append(p.name)

    return {
        "doc_id": doc_id,
        "figure_markers": md.count("[FIGURE "),
        "md_images": len(IMAGE_RE.findall(md)),
        "leaked_junk": leaked,
        "kept_images": kept,
        "orphan_good_pngs": orphans,
        "picture_text": md.count("Start of picture text"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate junk-image filtering")
    parser.add_argument("--doc", action="append", help="override validation set")
    parser.add_argument("--skip-convert", action="store_true")
    args = parser.parse_args()

    docs = args.doc or VALIDATION_DOCS
    py = sys.executable

    if not args.skip_convert:
        print("=== convert + annotate (force) ===")
        for doc_id in docs:
            run_step([py, "pdf_to_markdown.py", "--doc", doc_id, "--force"])
            run_step([py, "annotate_figures.py", "--doc", doc_id, "--force"])

    print("\n=== junk filter audit ===")
    total_leaked = 0
    for doc_id in docs:
        r = audit_doc(doc_id)
        leaked = r["leaked_junk"]
        total_leaked += len(leaked)
        status = "PASS" if not leaked else "FAIL"
        detail = f"markers={r['figure_markers']} kept={len(r['kept_images'])}"
        if leaked:
            detail += f" LEAKED={[x[1] for x in leaked]}"
        if r["orphan_good_pngs"]:
            detail += f" orphans={r['orphan_good_pngs'][:3]}"
        print(f"{status} {doc_id}: {detail}")

    print(f"\n{len(docs)} docs | junk leaked into output: {total_leaked}")
    if total_leaked:
        print("\nLeaked dimensions:")
        for doc_id in docs:
            for ref, name, w, h in audit_doc(doc_id)["leaked_junk"]:
                print(f"  {doc_id}/{name}: {w}×{h} ({ref})")
        raise SystemExit(1)
    print("All validation docs clean.")


if __name__ == "__main__":
    main()
