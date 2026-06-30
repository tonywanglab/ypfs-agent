"""
Query-side retrieval seam. Ported from ypfs-rag/harness/retrieval.py.

The corpus is embedded on the INGESTION side by `embed_chunks.py` (repo root).
This module is the QUERY side: it embeds a user query with the SAME
provider/model/dim the corpus was built with, queries Pinecone for the nearest
child/leaf chunks, and returns plain match dicts. Parent expansion happens in
`tools.py`.

Consistency is everything: a query vector from a different model or dimension
than the corpus returns nonsense. Provider/model/dim are set via env vars AND
asserted against what `embed_chunks.py` stamped into each Pinecone record, so a
mismatch fails loud instead of returning garbage.

Config (env, with defaults; MUST match what embed_chunks.py used):
  EMBED_PROVIDER   gemini | openrouter   (default: openrouter)
  EMBED_MODEL      model id              (default: openrouter's embedder default)
  EMBED_DIM        output dimension      (default: 1536)
  PINECONE_INDEX   index name            (default: ypfs-rag)
  PINECONE_NAMESPACE                     (default: "")
"""

import os
import sys
from pathlib import Path

# embed_chunks.py lives at the repo root; reuse its Embedder classes rather than
# re-implementing query embedding.
sys.path.insert(0, str(Path(__file__).parent.parent))


def make_query_embedder():
    """Build an Embedder whose vectors are compatible with the indexed corpus.

    Gemini is asymmetric: the corpus side uses RETRIEVAL_DOCUMENT, so the query
    side must use RETRIEVAL_QUERY. OpenRouter is symmetric (no task_type), so the
    same class serves both sides.
    """
    provider = os.getenv("EMBED_PROVIDER", "openrouter")
    model = os.getenv("EMBED_MODEL") or None
    dim = int(os.getenv("EMBED_DIM", "1536"))

    if provider == "gemini":
        from embed_chunks import GeminiEmbedder
        return GeminiEmbedder(
            dim=dim,
            model=model or "gemini-embedding-001",
            task_type="RETRIEVAL_QUERY",
        )
    if provider == "openrouter":
        from embed_chunks import OpenRouterEmbedder
        # Let the embedder apply its own default model when EMBED_MODEL is unset.
        return OpenRouterEmbedder(dim=dim) if model is None else OpenRouterEmbedder(dim=dim, model=model)
    raise SystemExit(f"unknown EMBED_PROVIDER: {provider!r} (expected gemini|openrouter)")


class PineconeRetriever:
    """Embeds a query and returns the nearest corpus chunks from Pinecone."""

    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise SystemExit(
                "PINECONE_API_KEY not set. Add it to .env. Get one at "
                "https://app.pinecone.io"
            )
        try:
            from pinecone import Pinecone
        except ImportError:
            raise SystemExit("pinecone not installed. Run:  pip install pinecone")

        self.index_name = os.getenv("PINECONE_INDEX", "ypfs-rag")
        self.namespace = os.getenv("PINECONE_NAMESPACE", "")
        self._index = Pinecone(api_key=api_key).Index(self.index_name)
        self._embedder = make_query_embedder()
        self._verified = False  # identity assertion runs once, on first hit

    def _verify_identity(self, metadata: dict) -> None:
        """Fail loud if the index was built with a different embedder than ours.

        embed_chunks.py stamps provider/model/dim onto every record; if those
        don't match this query embedder, every distance is meaningless.
        """
        stored = (
            metadata.get("provider"),
            metadata.get("model"),
            int(metadata["dim"]) if metadata.get("dim") is not None else None,
        )
        want = (self._embedder.name, self._embedder.model, self._embedder.dim)
        # Only assert when the index actually carries the stamp (older indexes won't).
        if stored[0] is not None and stored != want:
            raise SystemExit(
                f"Embedding mismatch — index '{self.index_name}' was built with "
                f"{stored} but the query embedder is {want}. They must be identical; "
                f"fix EMBED_PROVIDER/EMBED_MODEL/EMBED_DIM (or re-embed the corpus)."
            )

    def retrieve(self, query: str, document_type: str | None = None,
                 k: int = 5, fanout: int = 3) -> list[dict]:
        """Return up to k*fanout nearest matches as plain dicts.

        Fan out beyond k because many child hits collapse to the same parent
        section during expansion; the caller dedups down to ~k unique sections.
        """
        vector = self._embedder.embed([query])[0]
        flt = {"document_type": {"$eq": document_type}} if document_type else None
        resp = self._index.query(
            vector=vector,
            top_k=k * fanout,
            include_metadata=True,
            namespace=self.namespace,
            filter=flt,
        )

        # Normalize Pinecone's response object to plain dicts so callers don't
        # depend on SDK match types.
        raw = getattr(resp, "matches", None)
        if raw is None:
            raw = resp["matches"]
        out = []
        for m in raw:
            md = getattr(m, "metadata", None)
            if md is None:
                md = m.get("metadata", {})
            out.append({
                "id": getattr(m, "id", None) or m["id"],
                "score": float(getattr(m, "score", None) if getattr(m, "score", None)
                               is not None else m["score"]),
                "metadata": dict(md or {}),
            })

        if not self._verified and out:
            self._verify_identity(out[0]["metadata"])
            self._verified = True
        return out


# Module-level singleton: one Pinecone connection + one loaded embedder per process.
_RETRIEVER: PineconeRetriever | None = None


def get_retriever() -> PineconeRetriever:
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = PineconeRetriever()
    return _RETRIEVER
