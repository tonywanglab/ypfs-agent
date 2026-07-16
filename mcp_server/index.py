"""Build and hold the in-memory BM25 section index over the corpus.

The corpus root (markdown/, metadata/) sits one level above this package.
Sections are produced by splitting each markdown doc at header boundaries
(`sections.parse_sections`), tokenized with a dependency-free tokenizer, and
ranked with rank_bm25's BM25Okapi. Built once per process (lazy singleton).
"""

import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from .sections import parse_sections

# mcp_server/ lives at the repo root, so the corpus dirs are its parent.
BASE_DIR = Path(__file__).parent.parent
MARKDOWN_DIR = BASE_DIR / "markdown"
METADATA_DIR = BASE_DIR / "metadata"

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Small inline English stopword set — keeps BM25 focused on content terms
# without pulling in NLTK. Intentionally short; BM25's IDF already discounts
# very common terms, so this only needs to drop the highest-frequency glue words.
_STOPWORDS = frozenset(
    "a an and are as at be by for from has have in is it its of on or that the to "
    "was were will with this these those their they them then than which who whom "
    "but not no nor so such into over under between during about above below".split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase, split on word characters, drop stopwords."""
    return [t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


class CorpusIndex:
    """BM25 over header-split sections of markdown/."""

    def __init__(self) -> None:
        self.sections: list[dict] = []   # section records (see _build)
        self._bm25: BM25Okapi | None = None
        self._build()

    def _build(self) -> None:
        index_path = METADATA_DIR / "index.json"
        meta_index: dict = (
            json.loads(index_path.read_text(encoding="utf-8"))
            if index_path.exists() else {}
        )

        corpus_tokens: list[list[str]] = []
        for md_path in sorted(MARKDOWN_DIR.glob("*.md")):
            doc_id = md_path.stem
            meta = meta_index.get(doc_id, {})
            # index.json is a compact summary (doc_type/title/url only); read the
            # full per-doc record once per doc for publication_date.
            full_meta_path = METADATA_DIR / f"{doc_id}.json"
            publication_date = None
            if full_meta_path.exists():
                try:
                    publication_date = json.loads(
                        full_meta_path.read_text(encoding="utf-8")
                    ).get("publication_date")
                except json.JSONDecodeError:
                    pass
            for sec in parse_sections(md_path.read_text(encoding="utf-8")):
                breadcrumb = " > ".join(sec["section_path"])
                # Mirror chunk_documents' leaf_text style: breadcrumb + header + body.
                text = (
                    (breadcrumb + "\n\n" if breadcrumb else "")
                    + f"{sec['header_text']}\n\n{sec['body']}"
                )
                self.sections.append({
                    "doc_id": doc_id,
                    "document_type": meta.get("document_type"),
                    "title": meta.get("title"),
                    "publication_date": publication_date,
                    "section_path": sec["section_path"],
                    "page": sec["page"],
                    "text": text,
                })
                corpus_tokens.append(tokenize(text))

        # BM25Okapi requires a non-empty corpus.
        if corpus_tokens:
            self._bm25 = BM25Okapi(corpus_tokens)

    def search(self, query: str, document_type: str | None = None,
               limit: int = 5) -> dict:
        """Return the top-`limit` sections for `query`.

        {"results": [{doc_id, document_type, title, publication_date,
        section_path, score, text, page}], "total_found": int}. total_found
        counts sections with a positive score (after the optional
        document_type filter).
        """
        if self._bm25 is None:
            return {"results": [], "total_found": 0}

        scores = self._bm25.get_scores(tokenize(query))
        # (index, score) for sections passing the filter with a positive score.
        ranked = [
            (i, float(s)) for i, s in enumerate(scores)
            if s > 0 and (document_type is None
                          or self.sections[i]["document_type"] == document_type)
        ]
        ranked.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, score in ranked[:limit]:
            sec = self.sections[i]
            results.append({
                "doc_id": sec["doc_id"],
                "document_type": sec["document_type"],
                "title": sec["title"],
                "publication_date": sec["publication_date"],
                "section_path": sec["section_path"],
                "score": round(score, 4),
                "text": sec["text"],
                "page": sec["page"],
            })
        return {"results": results, "total_found": len(ranked)}


# Module-level singleton: one index per process.
_INDEX: CorpusIndex | None = None


def get_index() -> CorpusIndex:
    global _INDEX
    if _INDEX is None:
        _INDEX = CorpusIndex()
    return _INDEX
