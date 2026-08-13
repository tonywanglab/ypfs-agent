"""FastMCP server exposing lexical retrieval over the corpus (stdio transport).

Three tools, shaped to mirror agent/tools.py so the agent adapter is a clean
drop-in:
  - search_corpus(query, document_type?, limit=5) -> ranked sections
  - get_document(document_id)                      -> full markdown + metadata
  - list_documents(document_type?)                 -> browse the corpus
"""

import json
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .index import BASE_DIR, METADATA_DIR, get_index

mcp = FastMCP("ypfs-corpus")

MARKDOWN_DIR = BASE_DIR / "markdown"

DOCUMENT_TYPES = ["survey", "case_study", "lesson_learned", "article", "note"]


def _safe_id(doc_id: str, base: Path, suffix: str) -> Path:
    """Resolve doc_id to a path and reject any traversal outside base."""
    resolved = (base / f"{doc_id}{suffix}").resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise ValueError(f"Invalid document_id: {doc_id!r}")
    return resolved


@mcp.tool()
def search_corpus(query: str, document_type: Optional[str] = None,
                  limit: int = 5) -> dict:
    """Lexical (BM25) keyword search over header-split sections of the
    financial-crisis corpus. Returns the best-matching sections, each with its
    document, section_path breadcrumb, and full section text. Use get_document to read
    a source in full. Prefer document_type='survey' first. 

    Args:
        query: Natural-language / keyword search query.
        document_type: Optional filter — one of survey, case_study,
            lesson_learned, article, note.
        limit: Max results (default 5).
    """
    return get_index().search(query, document_type=document_type, limit=limit)


@mcp.tool()
def get_document(document_id: str) -> dict:
    """Retrieve the full markdown text and metadata of one document by its doc_id
    (e.g. from search_corpus results). Use to read a source in full.

    Args:
        document_id: The doc_id to fetch, e.g. vol1_iss1_2.
    """
    try:
        meta_path = _safe_id(document_id, METADATA_DIR, ".json")
        md_path = _safe_id(document_id, MARKDOWN_DIR, ".md")
    except ValueError as e:
        return {"error": str(e)}

    if not meta_path.exists():
        return {"error": f"Document not found: {document_id}"}

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
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


@mcp.tool()
def list_documents(document_type: Optional[str] = None) -> dict:
    """List documents in the corpus (doc_id, title, document_type, url),
    optionally filtered by document_type. Use to browse what is available before
    searching or reading.

    Args:
        document_type: Optional filter — one of survey, case_study,
            lesson_learned, article, note.
    """
    index_path = METADATA_DIR / "index.json"
    if not index_path.exists():
        return {"documents": [], "total": 0}

    meta_index = json.loads(index_path.read_text(encoding="utf-8"))
    documents = [
        {
            "doc_id": doc_id,
            "title": entry.get("title"),
            "document_type": entry.get("document_type"),
            "url": entry.get("url"),
        }
        for doc_id, entry in sorted(meta_index.items())
        if document_type is None or entry.get("document_type") == document_type
    ]
    return {"documents": documents, "total": len(documents)}
