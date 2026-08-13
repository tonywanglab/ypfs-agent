"""
Phase 3a: Enrich chunks with retrieval context before embedding.

For each embedded chunk (child + leaf), build an `embedding_text` field that
prepends contextual signals to the original chunk text so the eventual vector
captures more than the local prose:

  - the document title                      (a reference to the document's title)
  - the section header path                 (already present in `text` as a breadcrumb)
  - captions of any figures in the chunk    (a caption for a nearby figure)
  - captions of any table-image figures     (reused verbatim — no LLM)
  - a 1-2 sentence summary of inline tables  (a summary of the table nearby — LLM)

The original text is left untouched; only the new `embedding_text` field is added.
Parent chunks are never embedded, so they are copied through unchanged. 
Output mirrors Phase 2: one JSON-lines file per document in
`enriched_chunks/{doc_id}.jsonl`.

Table summaries are the only LLM calls. They follow the hybrid policy:
  - table-IMAGE figures ([FIGURE type=table ...]) reuse their existing caption;
  - inline markdown pipe tables (the actual data) are summarized by an LLM.
Summaries are cached on disk by table hash, so re-runs and duplicate tables are free.

Usage:
  python enrich_chunks.py --all
  python enrich_chunks.py --doc vol1_iss1_2
  python enrich_chunks.py --all --force          # overwrite existing enriched files
  python enrich_chunks.py --all --no-llm         # skip table summaries (no API calls)
  python enrich_chunks.py --doc vol2_iss3_1 --model anthropic/claude-haiku-4-5
"""

import argparse
import hashlib
import json
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

CHUNKS_DIR = Path("chunks")
ENRICHED_DIR = Path("enriched_chunks")
MARKDOWN_DIR = Path("markdown")
CACHE_PATH = ENRICHED_DIR / ".table_summary_cache.json"

# --- OpenRouter (same convention as benchmark.py / agent.py) ---
API_KEY = os.getenv("OR_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Cheap model by default — table summaries are short and there are many of them.
DEFAULT_MODEL = "anthropic/claude-haiku-4-5"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/rtstudios/ypfs-rag",
    "X-Title": "YPFS RAG chunk enrichment",
}

# Matches a single [FIGURE ...] marker and pulls out its attributes.
FIGURE_MARKER_RE = re.compile(r"\[FIGURE\s+([^\]]+)\]")
ATTR_RE = {
    "id": re.compile(r"\bid=(\S+)"),
    "type": re.compile(r"\btype=(\S+)"),
    "label": re.compile(r'\blabel="([^"]*)"'),
    "caption": re.compile(r'\bcaption="([^"]*)"'),
}

SUMMARY_PROMPT = (
    "You are summarizing a data table extracted from a financial-crisis research "
    "document so the summary can be embedded for semantic retrieval. In ONE or TWO "
    "sentences, state what the table reports: its subject, the key variables/columns, "
    "and the time period or entities covered if present. Do not invent values. "
    "Reply with the summary only — no preamble.\n\nTable:\n{table}"
)


# -------------------- figure captions --------------------
def parse_figure_markers(doc_id: str) -> dict[str, dict]:
    """Build {figure_id: {label, type, caption}} from the document's markdown.

    Captions live in the [FIGURE ...] markers inserted by annotate_figures.py.
    A chunk's `figure_refs` are looked up here to attach human-readable captions.
    """
    md_path = MARKDOWN_DIR / f"{doc_id}.md"
    if not md_path.exists():
        return {}

    figures: dict[str, dict] = {}
    for marker_body in FIGURE_MARKER_RE.findall(md_path.read_text(encoding="utf-8")):
        attrs = {}
        for key, rx in ATTR_RE.items():
            m = rx.search(marker_body)
            attrs[key] = m.group(1) if m else None
        if attrs["id"]:
            figures[attrs["id"]] = attrs
    return figures


# -------------------- inline tables --------------------
def extract_inline_tables(text: str) -> list[str]:
    """Return markdown pipe-table blocks found in the chunk text.

    A block is a run of >= 2 consecutive lines whose stripped form starts with '|'.
    These are real data tables (as opposed to table-IMAGE [FIGURE] markers) and are
    what gets LLM-summarized.
    """
    tables: list[str] = []
    run: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith("|"):
            run.append(line)
        else:
            if len(run) >= 2:
                tables.append("\n".join(run).strip())
            run = []
    if len(run) >= 2:
        tables.append("\n".join(run).strip())
    return tables


# -------------------- LLM table summary --------------------
def load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    ENRICHED_DIR.mkdir(exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=0), encoding="utf-8")


def table_key(table_md: str) -> str:
    return hashlib.sha1(table_md.encode("utf-8")).hexdigest()


def summarize_table(table_md: str, model: str, cache: dict, retries: int = 3) -> str | None:
    """Return a short LLM summary of a markdown table, using/filling the cache.

    Returns None on failure (caller then simply omits the summary for that table).
    """
    key = table_key(table_md)
    if key in cache:
        return cache[key]

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": SUMMARY_PROMPT.format(table=table_md)}],
        "temperature": 0.0,
    }
    for attempt in range(retries):
        try:
            resp = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=120)
            resp.raise_for_status()
            summary = resp.json()["choices"][0]["message"]["content"].strip()
            cache[key] = summary
            return summary
        except requests.exceptions.RequestException as e:
            wait = 2 ** attempt
            print(f"    table summary failed (attempt {attempt + 1}/{retries}): {e} — retrying in {wait}s")
            time.sleep(wait)
    print("    table summary giving up after retries — omitting")
    return None


# -------------------- enrichment --------------------
def build_embedding_text(chunk: dict, figures: dict[str, dict], model: str,
                         cache: dict, use_llm: bool) -> str:
    """Assemble the enriched text that will be embedded for this chunk."""
    lines: list[str] = []

    # 1. Document title reference.
    title = chunk.get("title")
    if title:
        lines.append(f"Document: {title}")

    # 2. Figure / table-image captions (reused verbatim — no LLM).
    for fig_id in chunk.get("figure_refs", []):
        fig = figures.get(fig_id)
        if not fig:
            continue
        label = fig.get("label") or fig.get("type") or "Figure"
        caption = fig.get("caption")
        kind = "Table" if fig.get("type") == "table" else "Figure"
        if caption:
            lines.append(f"{kind} — {label}: {caption}")
        else:
            lines.append(f"{kind} — {label}")

    # 3. Inline data-table summaries (LLM, hybrid policy).
    if use_llm:
        for table_md in extract_inline_tables(chunk["text"]):
            summary = summarize_table(table_md, model, cache)
            if summary:
                lines.append(f"Table summary: {summary}")

    # 4. The original chunk text (already carries the section-path breadcrumb).
    header = "\n".join(lines)
    return f"{header}\n\n{chunk['text']}" if header else chunk["text"]


def enrich_document(doc_id: str, model: str, use_llm: bool, force: bool, cache: dict) -> int:
    out_path = ENRICHED_DIR / f"{doc_id}.jsonl"
    if out_path.exists() and not force:
        return 0

    in_path = CHUNKS_DIR / f"{doc_id}.jsonl"
    if not in_path.exists():
        print(f"skipped {doc_id} — no chunks/{doc_id}.jsonl (run chunk_documents.py first)")
        return 0

    figures = parse_figure_markers(doc_id)
    enriched = []
    with open(in_path, encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            # Only child + leaf chunks are embedded; parents are fetched by ID.
            if chunk["chunk_type"] in ("child", "leaf"):
                chunk["embedding_text"] = build_embedding_text(
                    chunk, figures, model, cache, use_llm
                )
            enriched.append(chunk)

    ENRICHED_DIR.mkdir(exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for chunk in enriched:
            f.write(json.dumps(chunk) + "\n")

    return len(enriched)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enrich chunks/{doc_id}.jsonl into enriched_chunks/{doc_id}.jsonl"
    )
    parser.add_argument("--all", action="store_true", help="enrich all docs in chunks/")
    parser.add_argument("--doc", help="single doc id, e.g. vol1_iss1_2")
    parser.add_argument("--force", action="store_true", help="overwrite existing enriched files")
    parser.add_argument("--no-llm", action="store_true",
                        help="skip inline-table LLM summaries (captions only, no API calls)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter model for table summaries")
    args = parser.parse_args()

    use_llm = not args.no_llm
    if use_llm and not API_KEY:
        raise SystemExit("OR_API_KEY not set — add it to .env or pass --no-llm")

    if args.doc:
        doc_ids = [args.doc]
    elif args.all:
        doc_ids = [p.stem for p in sorted(CHUNKS_DIR.glob("*.jsonl"))]
    else:
        parser.print_help()
        return

    cache = load_cache()
    total_chunks = 0
    total_docs = 0
    try:
        for doc_id in doc_ids:
            n = enrich_document(doc_id, args.model, use_llm, args.force, cache)
            if n:
                print(f"enriched {doc_id}: {n} chunks")
                total_chunks += n
                total_docs += 1
                save_cache(cache)  # persist incrementally so a crash never loses summaries
    finally:
        save_cache(cache)

    if args.all or args.doc:
        print(f"done: {total_docs} docs | {total_chunks} total chunks")


if __name__ == "__main__":
    main()
