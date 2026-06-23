"""
Phase 2: Chunk markdown/ documents into overlapping text chunks for RAG ingestion.

Per-section routing (evaluated at each header boundary, not per document):
  section <= 300 tokens  -> leaf chunk (embedded directly, no parent)
  section >  300 tokens  -> parent chunk (full section text, fetched by ID at query time)
                         +  child chunks (~150 tokens, paragraph-boundary overlap, embedded)

Only child and leaf chunks go into the vector store. When a child is retrieved, its
parent_id is used to fetch the full section text to pass to the model.

Output: chunks/{doc_id}.jsonl — one JSON object per line per chunk.

Usage:
  python chunk_documents.py --all
  python chunk_documents.py --doc vol1_iss1_2
  python chunk_documents.py --all --force
"""

import argparse
import json
import re
from pathlib import Path

import tiktoken

MARKDOWN_DIR = Path("markdown")
CHUNKS_DIR = Path("chunks")
METADATA_DIR = Path("metadata")

SECTION_THRESHOLD = 300  # sections above this token count get parent+child split
CHILD_TARGET = 150       # target tokens per child chunk

enc = tiktoken.encoding_for_model("gpt-4o")

HEADER_RE = re.compile(r"^(#{1,6})\s+(.+)$")
PAGE_RE = re.compile(r"^--- end of page(?:\.page_number)?=(\d+) ---\s*$")
FIGURE_RE = re.compile(r"\[FIGURE id=(\S+)")


def count_tokens(text: str) -> int:
    return len(enc.encode(text))


def parse_sections(md_text: str) -> list[dict]:
    """Split markdown into sections at every header boundary.

    Returns a list of dicts, each with:
      header_text, header_level, body, page, section_path

    section_path is the list of active header texts (ancestor + self) at the
    point this section starts, used as a breadcrumb in child/leaf chunks.
    """
    lines = md_text.splitlines()
    sections = []
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
            # Flush the in-progress section before starting the new one, so that
            # active_headers still reflects the OLD section's context (not yet updated).
            if current is not None:
                body = "\n".join(current["body_lines"]).strip()
                if body:  # skip sections that are just a header with no body
                    path = [active_headers[lvl] for lvl in sorted(active_headers)]
                    sections.append({**current, "body": body, "section_path": path})

            level = len(header_m.group(1))
            # Strip bold markers that pymupdf4llm sometimes wraps around header text
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


def split_children(body: str, section_path: list[str]) -> list[str]:
    """Split body text into ~CHILD_TARGET-token chunks at paragraph boundaries.

    Prepends the section path breadcrumb to each child so embeddings capture
    document location, not just local semantics.

    Returns a list of child text strings. Each child overlaps the previous by
    one paragraph to avoid losing context at split boundaries.
    """
    paragraphs = [p.strip() for p in re.split(r"\n\n+", body) if p.strip()]
    if not paragraphs:
        return []

    breadcrumb = " > ".join(section_path) + "\n\n" if section_path else ""
    children = []
    i = 0

    while i < len(paragraphs):
        group: list[str] = []
        tokens = count_tokens(breadcrumb)
        j = i

        while j < len(paragraphs):
            p_tokens = count_tokens(paragraphs[j])
            # Only break if we already have content — always include at least one paragraph
            if group and tokens + p_tokens > CHILD_TARGET:
                break
            group.append(paragraphs[j])
            tokens += p_tokens
            j += 1

        children.append(breadcrumb + "\n\n".join(group))

        # Overlap by 1 paragraph (back up one step), but don't overlap at the end
        # and always advance by at least 1 to prevent an infinite loop on large paragraphs.
        if j >= len(paragraphs):
            i = j  # last group — no overlap needed
        else:
            i = max(i + 1, j - 1)

    return children


def make_chunk(
    chunk_id: str,
    parent_id: str | None,
    chunk_type: str,
    doc_id: str,
    meta: dict,
    text: str,
    page: int | None,
    section_path: list[str],
) -> dict:
    return {
        "chunk_id": chunk_id,
        "parent_id": parent_id,
        "chunk_type": chunk_type,  # "parent" | "child" | "leaf"
        "doc_id": doc_id,
        "document_type": meta.get("document_type"),
        "title": meta.get("title"),
        "text": text,
        "token_count": count_tokens(text),
        "section_path": section_path,
        "page": page,
        # IDs of any [FIGURE] markers that appear in this chunk's text
        "figure_refs": FIGURE_RE.findall(text),
    }


def chunk_document(doc_id: str, meta: dict, force: bool = False) -> int:
    out_path = CHUNKS_DIR / f"{doc_id}.jsonl"
    if out_path.exists() and not force:
        return 0

    md_path = MARKDOWN_DIR / f"{doc_id}.md"
    if not md_path.exists():
        print(f"skipped {doc_id} — no markdown/{doc_id}.md (run pdf_to_markdown.py first)")
        return 0

    sections = parse_sections(md_path.read_text(encoding="utf-8"))
    chunks = []
    seq = 0  # monotonic counter for unique IDs within this document

    for section in sections:
        # Full section text: header gives context when this section is fetched as a parent
        section_text = f"{section['header_text']}\n\n{section['body']}"
        tokens = count_tokens(section_text)

        if tokens <= SECTION_THRESHOLD:
            # Short section: single leaf chunk, embedded directly
            seq += 1
            breadcrumb = " > ".join(section["section_path"]) + "\n\n" if section["section_path"] else ""
            leaf_text = breadcrumb + section_text
            chunks.append(make_chunk(
                f"{doc_id}_l{seq:04d}", None, "leaf",
                doc_id, meta, leaf_text, section["page"], section["section_path"],
            ))
        else:
            # Long section: parent (full text) + children (small overlapping slices)
            seq += 1
            parent_id = f"{doc_id}_p{seq:04d}"
            chunks.append(make_chunk(
                parent_id, None, "parent",
                doc_id, meta, section_text, section["page"], section["section_path"],
            ))
            for child_text in split_children(section["body"], section["section_path"]):
                seq += 1
                chunks.append(make_chunk(
                    f"{doc_id}_c{seq:04d}", parent_id, "child",
                    doc_id, meta, child_text, section["page"], section["section_path"],
                ))

    CHUNKS_DIR.mkdir(exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + "\n")

    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk markdown/ docs into chunks/{doc_id}.jsonl")
    parser.add_argument("--all", action="store_true", help="chunk all docs in markdown/")
    parser.add_argument("--doc", help="single doc id, e.g. vol1_iss1_2")
    parser.add_argument("--force", action="store_true", help="overwrite existing chunk files")
    args = parser.parse_args()

    if not MARKDOWN_DIR.exists():
        raise SystemExit("markdown/ not found — run pdf_to_markdown.py first")

    index = json.loads((METADATA_DIR / "index.json").read_text(encoding="utf-8"))

    if args.doc:
        doc_ids = [args.doc]
    elif args.all:
        doc_ids = [p.stem for p in sorted(MARKDOWN_DIR.glob("*.md"))]
    else:
        parser.print_help()
        return

    total_chunks = 0
    total_docs = 0
    for doc_id in doc_ids:
        meta_path = METADATA_DIR / f"{doc_id}.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        n = chunk_document(doc_id, meta, force=args.force)
        if n:
            print(f"chunked {doc_id}: {n} chunks")
            total_chunks += n
            total_docs += 1

    if args.all or args.doc:
        print(f"done: {total_docs} docs | {total_chunks} total chunks")


if __name__ == "__main__":
    main()
