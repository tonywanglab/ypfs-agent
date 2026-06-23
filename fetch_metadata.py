"""
Phase 0: fetch and cache Digital Commons metadata for the JFC corpus.

Architecture:
  - One GET query (paginated) against the bepress Content-Out API
  - Normalize each record → metadata/{doc_id}.json
  - Build metadata/index.json for fast lookup

doc_id matches local filenames: vol2_iss3_14 from .../vol2/iss3/14
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

SITE = "elischolar.library.yale.edu"
BASE_URL = f"https://content-out.bepress.com/v2/{SITE}"
QUERY = 'publication_title:"Journal of Financial Crises"'
DOC_URL_RE = re.compile(
    r"/journal-of-financial-crises/vol(\d+)/iss(\d+)/(\d+)/?$", re.I
)

METADATA_DIR = Path("metadata")
PDF_DIR = Path("pdfs")

QUERY_PARAMS = {"q": QUERY}

# Slug (first element of API document_type list) → corpus label.
TYPE_MAP = {
    "article": "article",
    "archive_note": "note",
    "casestudy": "case_study",
    "lessons_learned": "lesson_learned",
    "note": "note",
    "survey": "survey",
}

PAGE_LIMIT = 100


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env")


def clean_token(raw: str) -> str:
    token = raw.strip()
    if token.lower().startswith("bearer "):
        token = token.split(" ", 1)[1].strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        token = token[1:-1]
    return token


def auth_headers() -> dict[str, str]:
    token = clean_token(os.environ.get("BEPRESS_API_TOKEN", ""))
    if not token:
        sys.exit(
            "Missing BEPRESS_API_TOKEN. Copy .env.example → .env and add your token."
        )

    auth_type = os.environ.get("BEPRESS_AUTH_TYPE", "raw").strip().lower()
    header_name = os.environ.get("BEPRESS_AUTH_HEADER", "").strip()

    if auth_type in ("api-key", "apikey", "x-api-key"):
        key = header_name or "x-api-key"
        return {key: token}

    if auth_type in ("raw", "none", "token"):
        return {"Authorization": token}

    # default: bearer
    scheme = os.environ.get("BEPRESS_AUTH_SCHEME", "Bearer").strip()
    return {"Authorization": f"{scheme} {token}"}


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    out = {}
    for key, val in headers.items():
        if len(val) <= 8:
            out[key] = "***"
        else:
            out[key] = f"{val[:4]}...{val[-4:]}"
    return out


def print_request_debug(path: str, params: dict | None) -> None:
    url = f"{BASE_URL}/{path.lstrip('/')}"
    headers = auth_headers()
    print("Request the script will send:")
    print(f"  method: GET")
    print(f"  url:    {url}")
    print(f"  params: {params}")
    print(f"  auth:   BEPRESS_AUTH_TYPE={os.environ.get('BEPRESS_AUTH_TYPE', 'raw')}")
    print(f"  headers (redacted): {redact_headers(headers)}")
    print(
        "\nCompare to Postman → Code → Python (requests).\n"
        "Match the Authorization / x-api-key header name and whether 'Bearer' is included."
    )


def explain_http_error(resp: requests.Response) -> None:
    body = resp.text.strip()
    print(f"\nHTTP {resp.status_code} from bepress API")
    print(f"URL: {resp.url}")
    if body:
        print(f"Response: {body[:500]}")

    if resp.status_code == 401:
        print(
            "\n401 = token missing or wrong header format.\n"
            "Postman often differs here. In Postman: Code → Python (requests) and match:\n"
            "  BEPRESS_AUTH_TYPE=bearer     → Authorization: Bearer <token>\n"
            "  BEPRESS_AUTH_TYPE=raw        → Authorization: <token> (no Bearer)\n"
            "  BEPRESS_AUTH_TYPE=api-key    → x-api-key: <token>\n"
            "  BEPRESS_AUTH_HEADER=My-Header  with BEPRESS_AUTH_TYPE=api-key for custom header names"
        )
    elif resp.status_code == 403:
        print(
            "\n403 = token was accepted by the gateway but lacks permission for this endpoint.\n"
            "This is usually NOT a code bug. Common causes:\n"
            "  • Token not provisioned for elischolar.library.yale.edu query access\n"
            "  • Token expired or revoked\n"
            "  • Wrong token type (e.g. admin UI token vs Content-Out API token)\n"
            "\nAsk Digital Commons / Yale for a Content-Out API v2 token scoped to:\n"
            f"  site: {SITE}\n"
            "  endpoint: query\n"
            "  publication: Journal of Financial Crises"
        )
    elif resp.status_code == 400:
        print(
            "\n400 = bad query. Use `q` for the search string only.\n"
            "Do NOT pass Solr `rows` — it is treated as a field name ('undefined field rows')."
        )
    sys.exit(1)


def api_get(path: str, params: dict | None = None) -> dict:
    url = f"{BASE_URL}/{path.lstrip('/')}"
    resp = requests.get(url, params=params or {}, headers=auth_headers(), timeout=120)
    if resp.status_code in (401, 403, 400):
        explain_http_error(resp)
    resp.raise_for_status()
    return resp.json()


def extract_docs(payload: dict) -> tuple[list[dict], int]:
    """Parse bepress v2 JSON (results/query_meta) or legacy Solr-style responses."""
    if "results" in payload:
        docs = payload["results"]
        meta = payload.get("query_meta") or {}
        total = meta.get("total_hits") or meta.get("total") or meta.get("numFound")
        if total is None:
            total = len(docs)
        return docs, int(total)

    if "response" in payload:
        body = payload["response"]
        return body.get("docs", []), int(body.get("numFound", len(body.get("docs", []))))

    if "docs" in payload:
        docs = payload["docs"]
        return docs, int(payload.get("numFound", len(docs)))

    if isinstance(payload, list):
        return payload, len(payload)

    raise ValueError(f"Unexpected API response shape: {list(payload.keys())}")


def first_str(record: dict, *keys: str) -> str | None:
    for key in keys:
        val = record.get(key)
        if val is None:
            continue
        if isinstance(val, list):
            val = val[0] if val else None
        if val:
            return str(val).strip()
    return None


def all_strs(record: dict, *keys: str) -> list[str]:
    for key in keys:
        val = record.get(key)
        if not val:
            continue
        if isinstance(val, str):
            return [val.strip()] if val.strip() else []
        if isinstance(val, list):
            return [str(v).strip() for v in val if str(v).strip()]
    return []


def doc_id_from_url(url: str | None) -> str | None:
    if not url:
        return None
    m = DOC_URL_RE.search(url)
    if not m:
        return None
    vol, iss, doc = m.groups()
    return f"vol{vol}_iss{iss}_{doc}"


def infer_document_type(record: dict) -> str | None:
    slugs = record.get("document_type") or []
    if isinstance(slugs, str):
        slugs = [slugs]
    if slugs:
        return TYPE_MAP.get(str(slugs[0]).strip().lower())
    return None


def normalize_record(record: dict) -> dict | None:
    url = first_str(
        record,
        "url",
        "article_url",
        "publication_url",
        "identifier_url",
        "fulltext_url",
    )
    doc_id = doc_id_from_url(url)
    if not doc_id:
        return None

    vol, iss, doc_num = DOC_URL_RE.search(url).groups()  # type: ignore[union-attr]

    authors = all_strs(record, "author", "authors", "author_lname")
    fname = all_strs(record, "author_fname")
    if authors and fname and len(authors) == len(fname):
        authors = [f"{fn} {ln}".strip() for fn, ln in zip(fname, authors)]

    return {
        "doc_id": doc_id,
        "document_type": infer_document_type(record),
        "title": first_str(record, "title", "article_title"),
        "authors": authors,
        "abstract": first_str(record, "abstract", "description", "comments"),
        "keywords": all_strs(record, "keywords", "keyword"),
        "publication_date": first_str(
            record, "publication_date", "date", "publication_year"
        ),
        "doi": first_str(record, "doi", "DOI"),
        "url": url,
        "download_link": first_str(record, "download_link"),
        "volume": int(vol),
        "issue": int(iss),
        "document_number": int(doc_num),
        "bepress_id": first_str(record, "id", "article_id", "articleid"),
        "raw": record,
    }


def fetch_all(save_raw: bool = False) -> list[dict]:
    """Fetch all records. Probe uses `q` only; full fetch paginates with start/limit."""
    all_docs: list[dict] = []
    start = 0
    total_hits = None

    while True:
        params = {**QUERY_PARAMS, "start": start, "limit": PAGE_LIMIT}
        payload = api_get("query", params)
        docs, total = extract_docs(payload)
        total_hits = total_hits or total

        if save_raw:
            raw_dir = METADATA_DIR / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            (raw_dir / f"page_{start}.json").write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )

        if not docs:
            break

        all_docs.extend(docs)
        print(f"  fetched {len(all_docs)}/{total_hits}")
        start += len(docs)
        if start >= total_hits:
            break

    return all_docs


def rebuild_index() -> int:
    """Rebuild metadata/index.json from existing metadata/vol*.json files."""
    index: dict[str, dict] = {}
    for path in sorted(METADATA_DIR.glob("vol*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        index[rec["doc_id"]] = {
            "path": str(path),
            "document_type": rec.get("document_type"),
            "title": rec.get("title"),
            "url": rec.get("url"),
        }
    (METADATA_DIR / "index.json").write_text(
        json.dumps(index, indent=2), encoding="utf-8"
    )
    return len(index)


def write_metadata(records: list[dict], force: bool = False) -> tuple[int, list[str]]:
    METADATA_DIR.mkdir(exist_ok=True)
    index: dict[str, dict] = {}
    written = 0
    unmapped_types: set[str] = set()

    for record in records:
        norm = normalize_record(record)
        if not norm:
            continue

        if norm["document_type"] is None:
            for key in ("publication_structure", "series_label", "series", "category"):
                raw = norm["raw"].get(key)
                if raw:
                    unmapped_types.add(f"{key}={raw!r}")

        out_path = METADATA_DIR / f"{norm['doc_id']}.json"
        if out_path.exists() and not force:
            pass
        else:
            out_path.write_text(json.dumps(norm, indent=2), encoding="utf-8")
            written += 1

        index[norm["doc_id"]] = {
            "path": str(out_path),
            "document_type": norm["document_type"],
            "title": norm["title"],
            "url": norm["url"],
        }

    (METADATA_DIR / "index.json").write_text(
        json.dumps(index, indent=2), encoding="utf-8"
    )
    return written, sorted(unmapped_types)


def validate_against_pdfs() -> list[str]:
    pdf_stems = {p.stem for p in PDF_DIR.glob("*.pdf")}
    meta_stems = {p.stem for p in METADATA_DIR.glob("vol*.json")}
    missing = sorted(pdf_stems - meta_stems)
    extra = sorted(meta_stems - pdf_stems)
    if missing:
        print(f"  PDFs without metadata: {len(missing)}")
        for stem in missing[:5]:
            print(f"    - {stem}")
        if len(missing) > 5:
            print(f"    ... and {len(missing) - 5} more")
    if extra:
        print(f"  Metadata without local PDF: {len(extra)}")
    if not missing and not extra:
        print("  All PDF stems matched metadata records.")
    return missing


def auth_test() -> None:
    """Check token presence and whether the API accepts it (no secret printed)."""
    token = clean_token(os.environ.get("BEPRESS_API_TOKEN", ""))
    if not token:
        sys.exit("Missing BEPRESS_API_TOKEN in .env")

    print(f"Token loaded: yes ({len(token)} chars)")
    print(f"Auth type: {os.environ.get('BEPRESS_AUTH_TYPE', 'raw')}")
    print(f"Site: {SITE}")
    print(f"Query: {QUERY}\n")
    print_request_debug("query", QUERY_PARAMS)

    url = f"{BASE_URL}/query"
    resp = requests.get(url, params=QUERY_PARAMS, headers=auth_headers(), timeout=120)
    print(f"GET /query → HTTP {resp.status_code}")
    if resp.ok:
        docs, total = extract_docs(resp.json())
        print(f"Success — numFound={total}, sample keys={sorted(docs[0].keys()) if docs else []}")
        return
    explain_http_error(resp)


def probe() -> None:
    """Fetch records and print field names — run this first to learn the API shape."""
    payload = api_get("query", QUERY_PARAMS)
    docs, total = extract_docs(payload)

    if "query_meta" in payload:
        print("query_meta:")
        print(json.dumps(payload["query_meta"], indent=2))

    print(f"\nresults: {len(docs)} returned, total={total}")
    if not docs:
        print("No records returned.")
        return

    record = docs[0]
    print("\nFirst result keys:")
    for key in sorted(record.keys()):
        val = record[key]
        preview = val if not isinstance(val, (list, dict)) else type(val).__name__
        print(f"  {key}: {preview!r}")

    norm = normalize_record(record)
    if norm:
        print("\nNormalized preview:")
        print(json.dumps({k: v for k, v in norm.items() if k != "raw"}, indent=2))
    else:
        print("\nCould not derive doc_id from first result — check URL field mapping.")


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser(description="Fetch JFC corpus metadata from bepress API")
    parser.add_argument("--auth-test", action="store_true", help="Check token + API permission")
    parser.add_argument("--print-request", action="store_true", help="Show request shape (token redacted)")
    parser.add_argument("--fetch", action="store_true", help="Fetch all records and write metadata/")
    parser.add_argument("--probe", action="store_true", help="Fetch 1 record and print field names")
    parser.add_argument("--validate", action="store_true", help="Compare metadata/ to pdfs/")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files")
    parser.add_argument("--save-raw", action="store_true", help="Cache raw API pages to metadata/raw/")
    parser.add_argument("--reindex", action="store_true", help="Rebuild index.json from metadata/vol*.json")
    args = parser.parse_args()

    if not any([args.auth_test, args.print_request, args.fetch, args.probe, args.validate, args.reindex]):
        parser.print_help()
        return

    if args.print_request:
        print_request_debug("query", QUERY_PARAMS)
        return

    if args.auth_test:
        auth_test()
    if args.probe:
        probe()
    if args.fetch:
        print("Fetching metadata...")
        records = fetch_all(save_raw=args.save_raw)
        written, unmapped = write_metadata(records, force=args.force)
        print(f"Wrote {written} metadata files ({len(records)} API records)")
        if unmapped:
            print("Unmapped document types (extend TYPE_MAP):")
            for item in unmapped[:20]:
                print(f"  {item}")
    if args.validate:
        validate_against_pdfs()
    if args.reindex:
        n = rebuild_index()
        print(f"Rebuilt index.json with {n} records")


if __name__ == "__main__":
    main()
