"""
Corpus ingestion: metadata (API) → PDF download → text extraction.

Pipeline:
  1. fetch_metadata.py  — bepress API → metadata/{doc_id}.json (includes download_link)
  2. download_all()     — download PDFs from metadata download_link → pdfs/
  3. extract_all()      — pypdf text extraction → text/

Legacy HTML issue-page scraping (collect_links) removed — use metadata API instead.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from pypdf import PdfReader

PDF_DIR = Path("pdfs")
TEXT_DIR = Path("text")
METADATA_DIR = Path("metadata")

failed_urls: list[tuple[str, str]] = []


def load_metadata() -> list[dict]:
    paths = sorted(METADATA_DIR.glob("vol*.json"))
    if not paths:
        sys.exit(
            "No metadata found in metadata/. Run:\n"
            "  python fetch_metadata.py --fetch"
        )
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]


def download_pdf(dest: Path, url: str) -> None:
    urllib.request.urlretrieve(url, dest)
    if not dest.read_bytes().startswith(b"%PDF"):
        dest.unlink(missing_ok=True)
        raise ValueError("response was not a PDF")


def download_all(records: list[dict], skip_existing: bool = True) -> None:
    PDF_DIR.mkdir(exist_ok=True)

    for rec in records:
        doc_id = rec["doc_id"]
        dest = PDF_DIR / f"{doc_id}.pdf"
        url = rec.get("download_link") or rec.get("raw", {}).get("download_link")

        if not url:
            print(f"skipped {doc_id} — no download_link in metadata")
            failed_urls.append((doc_id, "missing download_link"))
            continue

        if skip_existing and dest.exists() and dest.read_bytes().startswith(b"%PDF"):
            continue

        try:
            download_pdf(dest, url)
            print(f"saved {dest.name}")
        except urllib.error.HTTPError as e:
            print(f"failed {dest.name} — {e.code}: {e.reason}")
            failed_urls.append((doc_id, url))
        except (urllib.error.URLError, ValueError, OSError) as e:
            print(f"failed {dest.name}: {e}")
            failed_urls.append((doc_id, url))

        time.sleep(random.randrange(4, 11))


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        pages.append(f"--- Page {i} ---\n{text}")
    return "\n\n".join(pages)


def extract_all() -> None:
    TEXT_DIR.mkdir(exist_ok=True)
    for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
        try:
            text = extract_text(pdf_path)
        except Exception as e:
            print(f"skipped {pdf_path.name}: {e}")
            continue
        (TEXT_DIR / f"{pdf_path.stem}.txt").write_text(text, encoding="utf-8")
        print(f"extracted {pdf_path.stem}")


def fetch_metadata(force: bool = False) -> None:
    from fetch_metadata import fetch_all, load_env, write_metadata

    load_env()
    print("Fetching metadata from API...")
    records = fetch_all()
    written, unmapped = write_metadata(records, force=force)
    print(f"Wrote {written} metadata files ({len(records)} API records)")
    if unmapped:
        print("Unmapped document types (extend TYPE_MAP in fetch_metadata.py):")
        for item in unmapped[:10]:
            print(f"  {item}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download PDFs and extract text from metadata")
    parser.add_argument(
        "--fetch-metadata",
        action="store_true",
        help="Fetch metadata from bepress API first",
    )
    parser.add_argument("--download", action="store_true", help="Download PDFs from metadata/")
    parser.add_argument("--extract", action="store_true", help="Extract text from pdfs/ → text/")
    parser.add_argument(
        "--all",
        action="store_true",
        help="fetch-metadata + download + extract",
    )
    parser.add_argument(
        "--force-metadata",
        action="store_true",
        help="With --fetch-metadata, overwrite existing metadata files",
    )
    parser.add_argument(
        "--redownload",
        action="store_true",
        help="Re-download PDFs even if they already exist",
    )
    args = parser.parse_args()

    if not any([args.fetch_metadata, args.download, args.extract, args.all]):
        parser.print_help()
        return

    if args.fetch_metadata or args.all:
        fetch_metadata(force=args.force_metadata)

    records = load_metadata()
    print(f"Loaded {len(records)} metadata records")

    if args.download or args.all:
        print("Downloading PDFs...")
        download_all(records, skip_existing=not args.redownload)

    if args.extract or args.all:
        print("Extracting text...")
        extract_all()

    if failed_urls:
        print("\nFailed downloads:")
        for doc_id, url in failed_urls:
            print(f"  {doc_id}: {url}")


if __name__ == "__main__":
    main()
