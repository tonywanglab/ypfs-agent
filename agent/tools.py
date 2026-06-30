"""
Tool registry + RAG tools for the agent.

The registry is two parallel structures: TOOLS (the JSON schemas sent to the
model each turn) and _FNS (name -> Python implementation). `@tool(schema)`
appends to both; `dispatch` runs one call by name. Adding a tool is one
decorated function — no framework, no introspection magic.

RAG tools (search_corpus, get_document) are ported from
ypfs-rag/harness/corpus_exhibit_tools.py, trimmed to the retrieval core.
"""

import json
from pathlib import Path
from typing import Callable, Optional

# ---- Registry ----

TOOLS: list[dict] = []          # function-call schemas, sent to the model
_FNS: dict[str, Callable] = {}  # tool name -> implementation


def tool(schema: dict):
    """Register a tool: @tool(schema) over its implementation function.

    schema is the OpenRouter/OpenAI function-call shape:
      {"type": "function", "function": {"name", "description", "parameters"}}
    """
    def deco(fn: Callable) -> Callable:
        TOOLS.append(schema)
        _FNS[schema["function"]["name"]] = fn
        return fn
    return deco


def dispatch(name: str, args: dict) -> dict:
    """Run one tool call by name. Never raises — a bad call becomes a tool error
    the model can read and recover from."""
    fn = _FNS.get(name)
    if fn is None:
        return {"error": f"unknown tool: {name}"}
    try:
        return fn(**args)
    # SystemExit (a BaseException) is how the ported retrieval code signals config
    # errors (e.g. missing PINECONE_API_KEY); catch it too so a bad tool call
    # surfaces as data the model can read, instead of killing the loop.
    except (Exception, SystemExit) as e:
        return {"error": f"{type(e).__name__}: {e}"}


# ---- Corpus paths + chunk index (ported) ----

BASE_DIR = Path(__file__).parent.parent  # repo root (markdown/, metadata/ live here)


def _safe_id(doc_id: str, base: Path, suffix: str) -> Path:
    """Resolve doc_id to a path and reject any traversal outside base."""
    resolved = (base / f"{doc_id}{suffix}").resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise ValueError(f"Invalid document_id: {doc_id!r}")
    return resolved


# chunks/ holds parent sections; it's a gitignored build artifact and may be
# absent. When it is, the index is empty and search_corpus falls back to the
# embedding_text stamped in each Pinecone record — degraded but still useful.
_CHUNK_BY_ID: dict[str, dict] | None = None


def _get_chunk_index() -> dict[str, dict]:
    """chunk_id -> chunk, across all docs. Empty if chunks/ isn't on disk."""
    global _CHUNK_BY_ID
    if _CHUNK_BY_ID is None:
        _CHUNK_BY_ID = {}
        for path in (BASE_DIR / "chunks").glob("*.jsonl"):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        c = json.loads(line)
                        _CHUNK_BY_ID[c["chunk_id"]] = c
    return _CHUNK_BY_ID


# ---- RAG tools ----

@tool({
    "type": "function",
    "function": {
        "name": "search_corpus",
        "description": (
            "Semantic search over the financial-crisis corpus. The query is "
            "embedded and matched against indexed chunks; each hit is expanded "
            "to its full parent section and deduplicated. Prefer document_type="
            "'survey' first. Use this before asserting facts about the corpus."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language search query."},
                "document_type": {
                    "type": "string",
                    "enum": ["survey", "case_study", "lesson_learned", "article", "note"],
                    "description": "Optional filter by document type.",
                },
                "limit": {"type": "integer", "description": "Max results (default 5)."},
            },
            "required": ["query"],
        },
    },
})
def search_corpus(query: str, document_type: Optional[str] = None, limit: int = 5) -> dict:
    """Embed + Pinecone search, then expand child hits to parent sections.

    Returns {"results": [{doc_id, chunk_id, document_type, title, score, text,
    matched_text, page, parent_id}], "total_found": int}. "text" is the parent
    section (or the Pinecone embedding_text when chunks/ is absent).
    """
    from .retrieval import get_retriever

    matches = get_retriever().retrieve(query, document_type=document_type, k=limit)
    by_id = _get_chunk_index()

    results: list[dict] = []
    seen_sections: set[str] = set()
    for m in matches:
        md = m["metadata"]
        chunk_id = m["id"]
        parent_id = md.get("parent_id")

        # Collapse all children of one parent into a single section result.
        section_key = parent_id or chunk_id
        if section_key in seen_sections:
            continue
        seen_sections.add(section_key)

        matched = by_id.get(chunk_id, {})
        # Expand child -> parent; leaf chunks have no parent, so use themselves.
        section = (by_id.get(parent_id) if parent_id else matched) or matched

        results.append({
            "doc_id": md.get("doc_id") or matched.get("doc_id"),
            "chunk_id": chunk_id,
            "document_type": md.get("document_type") or matched.get("document_type"),
            "title": md.get("title") or matched.get("title"),
            "score": round(m["score"], 4),
            "text": section.get("text", "") if section else md.get("embedding_text", ""),
            "matched_text": matched.get("text", "")[:800],
            "page": md.get("page") or matched.get("page"),
            "parent_id": parent_id,
        })
        if len(results) >= limit:
            break

    return {"results": results, "total_found": len(matches)}


@tool({
    "type": "function",
    "function": {
        "name": "get_document",
        "description": (
            "Retrieve the full text and metadata of one document by its doc_id "
            "(from search_corpus results). Use to read a source in full."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "document_id": {"type": "string", "description": "The doc_id to fetch."},
            },
            "required": ["document_id"],
        },
    },
})
def get_document(document_id: str) -> dict:
    """Return full markdown + metadata for a doc_id, with a traversal guard."""
    try:
        meta_path = _safe_id(document_id, BASE_DIR / "metadata", ".json")
        md_path = _safe_id(document_id, BASE_DIR / "markdown", ".md")
    except ValueError as e:
        return {"error": str(e)}

    if not meta_path.exists():
        return {"error": f"Document not found: {document_id}"}

    meta = json.loads(meta_path.read_text())
    text = md_path.read_text() if md_path.exists() else ""
    return {
        "doc_id": document_id,
        "document_type": meta.get("document_type"),
        "title": meta.get("title"),
        "authors": meta.get("authors", []),
        "abstract": meta.get("abstract"),
        "publication_date": meta.get("publication_date"),
        "url": meta.get("url"),
        "text": text,
    }
