"""
Phase 1a: PDF → Markdown via pymupdf4llm (layout, headers, lists, tables, images).

Output: markdown/{doc_id}.md with images under assets/{doc_id}/.
Pair with annotate_figures.py to insert [FIGURE] markers (Phase 1b).
"""

from __future__ import annotations

import argparse
import gc
import shutil
import sys
from pathlib import Path

import pymupdf
import pymupdf4llm

from figure_filters import clean_pymupdf4llm_markdown

PDF_DIR = Path("pdfs")
MARKDOWN_DIR = Path("markdown")
ASSETS_DIR = Path("assets")

# Skip EliScholar boilerplate (cover + notice) on most JFC PDFs.
DEFAULT_SKIP_PAGES = 2
MIN_CHARS_PER_PAGE = 400
DEFAULT_MIN_FREE_MB = 1024


def flush_pymupdf_cache() -> None:
    """Drop PyMuPDF pixmap store between documents to limit disk/RAM cache growth."""
    pymupdf.TOOLS.store_shrink(100)
    gc.collect()


def disk_free_mb() -> float:
    return shutil.disk_usage(".").free / (1024 * 1024)


def ensure_disk_headroom(min_free_mb: float) -> None:
    free = disk_free_mb()
    if free < min_free_mb:
        raise OSError(
            28,
            f"insufficient disk headroom: {free:.0f}MB free, need {min_free_mb:.0f}MB "
            f"(set --min-free-mb or free space and resume)",
        )


def _clear_asset_dir(assets_dir: Path) -> None:
    if assets_dir.exists():
        shutil.rmtree(assets_dir)
    assets_dir.mkdir(parents=True, exist_ok=True)


def _to_markdown(pdf_path: Path, pages: list[int] | None, assets_dir: Path) -> str:
    return pymupdf4llm.to_markdown(
        str(pdf_path),
        pages=pages,
        header=False,
        footer=False,
        write_images=True,
        image_path=str(assets_dir),
        image_format="png",
        page_separators=True,
        use_ocr=False,
    )


def convert_pdf(
    pdf_path: Path,
    skip_pages: int = DEFAULT_SKIP_PAGES,
    force: bool = False,
    min_free_mb: float = DEFAULT_MIN_FREE_MB,
) -> Path | None:
    ensure_disk_headroom(min_free_mb)

    doc_id = pdf_path.stem
    out_path = MARKDOWN_DIR / f"{doc_id}.md"
    if out_path.exists() and not force:
        return None

    doc = pymupdf.open(pdf_path)
    page_count = doc.page_count
    doc.close()

    pages = list(range(skip_pages, page_count)) if skip_pages else None
    assets_dir = ASSETS_DIR / doc_id
    assets_dir.mkdir(parents=True, exist_ok=True)

    expected_pages = len(pages) if pages else page_count
    md = _to_markdown(pdf_path, pages, assets_dir)
    if expected_pages and len(md) / expected_pages < MIN_CHARS_PER_PAGE:
        # Retry once without duplicating extracted PNGs on disk.
        _clear_asset_dir(assets_dir)
        md = _to_markdown(pdf_path, pages, assets_dir)

    md, removed = clean_pymupdf4llm_markdown(md, doc_id, ASSETS_DIR)
    if removed:
        print(f"  dropped {removed} junk/unreferenced image(s) for {doc_id}")

    MARKDOWN_DIR.mkdir(exist_ok=True)
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(md, encoding="utf-8")
    tmp.replace(out_path)
    flush_pymupdf_cache()
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert PDFs to Markdown (pymupdf4llm)")
    parser.add_argument("--all", action="store_true", help="Convert all pdfs/")
    parser.add_argument("--doc", help="Single doc id, e.g. vol2_iss3_14")
    parser.add_argument("--force", action="store_true", help="Overwrite existing markdown")
    parser.add_argument(
        "--skip-pages",
        type=int,
        default=DEFAULT_SKIP_PAGES,
        help=f"Skip first N pages (default {DEFAULT_SKIP_PAGES}, journal boilerplate)",
    )
    parser.add_argument(
        "--no-skip",
        action="store_true",
        help="Include all pages from page 1",
    )
    parser.add_argument(
        "--min-free-mb",
        type=float,
        default=DEFAULT_MIN_FREE_MB,
        help=f"Stop batch if free disk drops below this (default {DEFAULT_MIN_FREE_MB}MB)",
    )
    args = parser.parse_args()

    skip = 0 if args.no_skip else args.skip_pages

    if args.doc:
        pdfs = [PDF_DIR / f"{args.doc}.pdf"]
    elif args.all:
        pdfs = sorted(PDF_DIR.glob("*.pdf"))
    else:
        parser.print_help()
        return

    if not pdfs:
        sys.exit("No PDFs found.")

    converted = skipped = failed = 0
    for pdf_path in pdfs:
        if not pdf_path.exists():
            print(f"missing {pdf_path.name}")
            failed += 1
            continue
        try:
            result = convert_pdf(
                pdf_path,
                skip_pages=skip,
                force=args.force,
                min_free_mb=args.min_free_mb,
            )
            if result:
                print(f"converted {pdf_path.stem}")
                converted += 1
            else:
                skipped += 1
        except OSError as e:
            if e.errno == 28:
                print(f"stopped {pdf_path.stem}: {e.strerror or e}")
                print(
                    f"disk headroom exhausted ({disk_free_mb():.0f}MB free); "
                    f"free space and rerun to resume"
                )
                break
            print(f"failed {pdf_path.stem}: {e}")
            failed += 1
        except Exception as e:
            print(f"failed {pdf_path.stem}: {e}")
            failed += 1

    print(f"done: {converted} converted, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
