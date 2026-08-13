"""
Phase 3b: Embed enriched chunks into vectors and load them into a vector store.

This is the step after `enrich_chunks.py`. For every embedded chunk (child +
leaf) it takes the `embedding_text` field, turns it into a dense vector with an
embedding model, and writes that vector — plus retrieval metadata — to a sink
(a local JSONL file, or directly into Pinecone).

Parents are never embedded (they are fetched by ID at answer time), so they are
skipped here just as they were left bare in enrichment.

Usage:
  # 1. Local file sink (no DB, no cost beyond the embedding API) — good first run.
  #    The default provider is OpenRouter + openai/text-embedding-3-small @ 1536d,
  #    so it can be omitted:
  python embed_chunks.py --all --sink jsonl

  # 2. Straight into Pinecone:
  python embed_chunks.py --all --sink pinecone --index ypfs-rag

  # 3. Native Google API instead of OpenRouter (adds task_type=RETRIEVAL_DOCUMENT
  #    for a retrieval-quality bump, but needs a separate GEMINI_API_KEY):
  python embed_chunks.py --all --provider gemini --sink jsonl

  # 4. Open-weights, fully local (needs a GPU for the 8B; 0.6B runs on CPU):
  python embed_chunks.py --all --provider qwen --qwen-model Qwen/Qwen3-Embedding-0.6B --sink jsonl

  # Single doc / smaller dimension (Matryoshka truncation) / overwrite:
  python embed_chunks.py --doc vol1_iss1_2 --dim 768 --sink jsonl --force

Whichever provider/model/dim you embed with here MUST match the query side
(EMBED_PROVIDER / EMBED_MODEL / EMBED_DIM in harness/retrieval.py), or retrieval
aborts on an embedding-identity mismatch. The defaults on both sides agree.

Required keys (see the printed hint on startup if one is missing):
  OR_API_KEY       for --provider openrouter (the default)
  GEMINI_API_KEY   for --provider gemini
  PINECONE_API_KEY for --sink pinecone
"""

import argparse
import json
import math
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ENRICHED_DIR = Path("enriched_chunks")
EMBEDDINGS_DIR = Path("embeddings")

# Metadata fields copied from each chunk onto its vector record. Kept small so it
# fits comfortably inside Pinecone's 40 KB/record metadata budget while still
# giving the retriever everything it needs to show and trace a hit.
META_FIELDS = ("doc_id", "document_type", "chunk_type", "title", "page", "parent_id")


# ============================================================================
#  Embedders  (the "model agnostic" seam — closed Gemini vs open Qwen3)
# ============================================================================
class Embedder:
    """Common interface. `embed(texts)` -> list[list[float]] of length len(texts)."""

    name: str          # provider id, stored on every record (e.g. "gemini")
    model: str         # concrete model id, stored on every record
    dim: int           # vector dimension actually produced

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


def _parse_retry_delay(msg: str) -> float | None:
    """Pull the suggested wait (seconds) out of a Gemini 429 error message.

    The API returns either "Please retry in 11.6s" or a "retryDelay": "11s"
    field; we read whichever is present so we sleep exactly as long as asked.
    """
    m = re.search(r"retry in ([\d.]+)s", msg) or re.search(r"retryDelay['\"]?:?\s*['\"]?([\d.]+)s", msg)
    return float(m.group(1)) if m else None


def _l2_normalize(vec: list[float]) -> list[float]:
    """Unit-normalize a vector (so cosine == dot product).

    Gemini does NOT auto-normalize when you truncate below 3072 dims, and Qwen
    benefits from it too, so we always normalize. A vector store using cosine
    distance then behaves identically regardless of provider.
    """
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


class GeminiEmbedder(Embedder):
    """Closed, hosted embeddings via the Gemini API (`gemini-embedding-001`).

    - No GPU, no model download; you pay ~$0.15 / 1M input tokens (batch: half).
    - Matryoshka model: `output_dimensionality` can be 3072 (default), 1536, or
      768 to trade a little accuracy for big storage savings, no re-training.
    - `task_type=RETRIEVAL_DOCUMENT` tells the model these are corpus passages.
      The RETRIEVAL SIDE (the query) must be embedded with RETRIEVAL_QUERY — do
      that in the retrieval script, not here.
    """

    name = "gemini"

    def __init__(self, dim: int = 3072, model: str = "gemini-embedding-001",
                 batch_size: int = 100, rpm: int = 90, max_retries: int = 6,
                 task_type: str = "RETRIEVAL_DOCUMENT"):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise SystemExit(
                "GEMINI_API_KEY not set. Add it to .env (this script will not edit "
                ".env for you). Get one at https://aistudio.google.com/apikey"
            )
        try:
            from google import genai
            from google.genai import types
            from google.genai import errors as genai_errors
        except ImportError:
            raise SystemExit(
                "google-genai not installed. Run:  pip install google-genai\n"
                "(not added to requirements.txt for you — flag for the owner.)"
            )
        self._genai = genai
        self._types = types
        self._errors = genai_errors
        self._client = genai.Client(api_key=api_key)
        self.model = model
        self.dim = dim
        # RETRIEVAL_DOCUMENT for the corpus (ingestion); the query side passes
        # RETRIEVAL_QUERY so the two halves of the retrieval are paired.
        self.task_type = task_type
        self.batch_size = batch_size
        self.max_retries = max_retries
        # Client-side throttle. The free tier allows 100 embed requests/minute,
        # and one embed_content call = ONE request no matter how many texts are
        # batched in it. Spacing calls keeps us under the cap so we (mostly)
        # never hit a 429 in the first place; --rpm 0 disables the throttle.
        self._min_interval = (60.0 / rpm) if rpm else 0.0
        self._last_call = 0.0

    def _embed_once(self, batch: list[str], cfg):
        """One embed_content call, throttled and retried on 429/5xx."""
        for attempt in range(self.max_retries):
            if self._min_interval:
                wait = self._min_interval - (time.monotonic() - self._last_call)
                if wait > 0:
                    time.sleep(wait)
            try:
                self._last_call = time.monotonic()
                return self._client.models.embed_content(
                    model=self.model, contents=batch, config=cfg
                )
            except self._errors.ClientError as e:
                # 429 = rate/quota. Honor the server's suggested retryDelay if present.
                if getattr(e, "code", None) != 429 or attempt == self.max_retries - 1:
                    raise
                delay = _parse_retry_delay(str(e)) or (2 ** attempt)
                print(f"    429 rate-limited — sleeping {delay:.0f}s "
                      f"(retry {attempt + 1}/{self.max_retries})")
                time.sleep(delay)
            except self._errors.ServerError as e:
                if attempt == self.max_retries - 1:
                    raise
                delay = 2 ** attempt
                print(f"    server error {getattr(e, 'code', '?')} — retrying in {delay}s")
                time.sleep(delay)
        raise RuntimeError("unreachable")  # loop either returns or raises

    # Gemini rejects inputs over 2,048 tokens (a 400, not a 429). token_count in
    # our chunks comes from tiktoken, not Gemini's tokenizer, so a chunk near the
    # limit can still trip it. ~4 chars/token is a safe rule of thumb; cap a hair
    # under the limit so one oversized chunk can't 400 the whole run.
    MAX_INPUT_CHARS = 2000 * 4

    def embed(self, texts: list[str]) -> list[list[float]]:
        cfg = self._types.EmbedContentConfig(
            task_type=self.task_type,
            output_dimensionality=self.dim,
        )
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = []
            for t in texts[i : i + self.batch_size]:
                if len(t) > self.MAX_INPUT_CHARS:
                    print(f"    truncating an oversized chunk "
                          f"({len(t)} chars) to fit the 2048-token input cap")
                    t = t[: self.MAX_INPUT_CHARS]
                batch.append(t)
            resp = self._embed_once(batch, cfg)
            out.extend(_l2_normalize(list(e.values)) for e in resp.embeddings)
        return out


class OpenRouterEmbedder(Embedder):
    """Hosted embeddings via OpenRouter's OpenAI-compatible endpoint.

    Default model is `openai/text-embedding-3-small` (~$0.02 / 1M input tokens,
    native 1536 dims) — chosen for the simplicity of ONE OpenRouter key for both
    chat and embeddings. OpenRouter only speaks the OpenAI embeddings schema
    (`model`, `input`, `encoding_format`), which costs two features versus the
    native GeminiEmbedder path:
      - No `task_type`. We cannot ask for RETRIEVAL_DOCUMENT, so vectors are the
        model's generic (symmetric) mode. Embed your QUERIES through OpenRouter
        too so both sides of the retrieval match. If retrieval quality suffers,
        switch to --provider gemini, which adds the asymmetric task_type.
      - No server-side `output_dimensionality`. We replicate Matryoshka
        truncation client-side: slice to `dim` and re-normalize. This is valid
        for both gemini-embedding-001 and OpenAI's text-embedding-3 family, which
        officially support shortening by slice + renormalize. `--dim 768/1536`
        works, it just happens locally.
    Vectors are L2-normalized here regardless of dim (OpenRouter does not
    guarantee unit length), so a cosine store behaves like the other providers.
    """

    name = "openrouter"
    API_URL = "https://openrouter.ai/api/v1/embeddings"
    # Ceiling for client-side Matryoshka truncation: a request for a smaller dim
    # is sliced, a larger one is left alone. Set high enough to cover every model
    # we route to (gemini-embedding-001 = 3072, text-embedding-3-* <= 3072) so it
    # never truncates a model's full-width output by accident.
    NATIVE_DIM = 3072
    # text-embedding-3-small caps input at ~8191 tokens and gemini-embedding-001
    # at ~2048; ~4 chars/token, a hair under the tighter limit (our token_count
    # is tiktoken's, so a chunk near the limit can still trip a 400 — truncate
    # defensively to the smaller cap to stay safe for either model).
    MAX_INPUT_CHARS = 2000 * 4

    def __init__(self, dim: int | None = None,
                 model: str = "openai/text-embedding-3-small",
                 batch_size: int = 100, rpm: int = 90, max_retries: int = 6):
        api_key = os.getenv("OR_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise SystemExit(
                "OR_API_KEY not set. Add it to .env (this script will not edit "
                ".env for you). Get one at https://openrouter.ai/keys"
            )
        self.model = model
        self.dim = dim or self.NATIVE_DIM
        # Matryoshka truncation: only when a smaller dim than native is asked.
        self._truncate_to = dim if (dim and dim < self.NATIVE_DIM) else None
        self.batch_size = batch_size
        self.max_retries = max_retries
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })
        # Same client-side throttle as GeminiEmbedder: one POST = one request
        # no matter how many texts are batched in it. --rpm 0 disables it.
        self._min_interval = (60.0 / rpm) if rpm else 0.0
        self._last_call = 0.0

    def _embed_once(self, batch: list[str]) -> list[list[float]]:
        """One embeddings POST, throttled and retried on 429/5xx."""
        payload = {"model": self.model, "input": batch, "encoding_format": "float"}
        for attempt in range(self.max_retries):
            if self._min_interval:
                wait = self._min_interval - (time.monotonic() - self._last_call)
                if wait > 0:
                    time.sleep(wait)
            self._last_call = time.monotonic()
            resp = self._session.post(self.API_URL, json=payload, timeout=120)
            if resp.status_code == 429 or resp.status_code >= 500:
                if attempt == self.max_retries - 1:
                    resp.raise_for_status()
                # Honor Retry-After (seconds) if the server sends one, else backoff.
                retry_after = resp.headers.get("Retry-After", "")
                delay = (float(retry_after)
                         if retry_after.replace(".", "", 1).isdigit()
                         else 2 ** attempt)
                tag = ("429 rate-limited" if resp.status_code == 429
                       else f"server error {resp.status_code}")
                print(f"    {tag} — sleeping {delay:.0f}s "
                      f"(retry {attempt + 1}/{self.max_retries})")
                time.sleep(delay)
                continue
            if not resp.ok:
                raise RuntimeError(
                    f"OpenRouter embeddings failed ({resp.status_code}): "
                    f"{resp.text[:500]}"
                )
            data = resp.json()["data"]
            # OpenAI-schema responses carry an `index`; sort so vectors line up
            # with their input texts even if the provider returns them unordered.
            data.sort(key=lambda d: d.get("index", 0))
            return [d["embedding"] for d in data]
        raise RuntimeError("unreachable")  # loop either returns or raises

    def embed(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = []
            for t in texts[i : i + self.batch_size]:
                if len(t) > self.MAX_INPUT_CHARS:
                    print(f"    truncating an oversized chunk "
                          f"({len(t)} chars) to fit the ~2048-token input cap")
                    t = t[: self.MAX_INPUT_CHARS]
                batch.append(t)
            for vec in self._embed_once(batch):
                if self._truncate_to:
                    vec = vec[: self._truncate_to]
                out.append(_l2_normalize(vec))
        return out


class QwenEmbedder(Embedder):
    """Open-weights embeddings run locally via sentence-transformers (Qwen3).

    - You own the weights (Apache-2.0): no per-token cost, data never leaves your
      machine, and the model can't be deprecated out from under you. The price is
      ops — the 8B wants ~16 GB GPU VRAM; the 0.6B runs on CPU (slowly).
    - Native dims: 0.6B=1024, 4B=2560, 8B=4096. Qwen3 also supports Matryoshka
      truncation; if `dim` is set below native we slice + renormalize.
    """

    name = "qwen"

    def __init__(self, model: str = "Qwen/Qwen3-Embedding-0.6B",
                 dim: int | None = None, batch_size: int = 32):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise SystemExit(
                "sentence-transformers not installed. Run:\n"
                "  pip install sentence-transformers torch\n"
                "(not added to requirements.txt for you — flag for the owner.)"
            )
        self._st = SentenceTransformer(model)
        self.model = model
        self.batch_size = batch_size
        native = self._st.get_sentence_embedding_dimension()
        self.dim = dim or native
        self._truncate_to = dim if (dim and dim < native) else None

    def embed(self, texts: list[str]) -> list[list[float]]:
        # normalize_embeddings=True gives unit vectors; documents need no prompt.
        vecs = self._st.encode(
            texts, batch_size=self.batch_size, normalize_embeddings=True,
            show_progress_bar=False, convert_to_numpy=True,
        )
        out = []
        for v in vecs:
            v = v.tolist()
            if self._truncate_to:
                v = _l2_normalize(v[: self._truncate_to])
            out.append(v)
        return out


# Default output dimension for the hosted Matryoshka providers (gemini /
# openrouter). MUST match EMBED_DIM on the query side (harness/retrieval.py),
# or _verify_identity aborts every retrieval as an embedding mismatch. 1536 is
# the sweet spot: half the storage of native 3072 for a negligible recall hit.
DEFAULT_HOSTED_DIM = 1536


def make_embedder(args) -> Embedder:
    if args.provider == "openrouter":
        return OpenRouterEmbedder(dim=args.dim or DEFAULT_HOSTED_DIM, model=args.or_model,
                                  batch_size=args.batch_size, rpm=args.rpm)
    if args.provider == "gemini":
        return GeminiEmbedder(dim=args.dim or DEFAULT_HOSTED_DIM,
                              batch_size=args.batch_size, rpm=args.rpm)
    if args.provider == "qwen":
        return QwenEmbedder(model=args.qwen_model, dim=args.dim, batch_size=args.batch_size)
    raise SystemExit(f"unknown provider: {args.provider}")


# ============================================================================
#  Sinks  (the "store agnostic" seam — local file vs Pinecone)
# ============================================================================
class Sink:
    def write(self, doc_id: str, records: list[dict]) -> None:
        raise NotImplementedError

    def already_done(self, doc_id: str) -> bool:
        return False

    def close(self) -> None:
        pass


class JsonlSink(Sink):
    """Write vectors to embeddings/{doc_id}.jsonl. Portable, free, re-loadable.

    Each line: {id, vector, provider, model, dim, metadata, embedding_text}.
    This is the format you'd later stream into Pinecone OR S3 Vectors, so it
    keeps your options open and lets you eyeball results before paying a DB.
    """

    def __init__(self, force: bool):
        self.force = force
        EMBEDDINGS_DIR.mkdir(exist_ok=True)

    def already_done(self, doc_id: str) -> bool:
        return (EMBEDDINGS_DIR / f"{doc_id}.jsonl").exists() and not self.force

    def write(self, doc_id: str, records: list[dict]) -> None:
        out = EMBEDDINGS_DIR / f"{doc_id}.jsonl"
        with open(out, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")


class PineconeSink(Sink):
    """Upsert vectors straight into a Pinecone serverless index.

    The index is created on first run (cosine metric, dimension = embedder.dim).
    Upserts are idempotent by chunk id, so re-running is safe (no skip logic
    needed). Metadata is trimmed to META_FIELDS + section_path + text so each
    record stays under Pinecone's 40 KB metadata cap.
    """

    def __init__(self, index_name: str, dim: int, namespace: str):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise SystemExit(
                "PINECONE_API_KEY not set. Add it to .env (this script will not "
                "edit .env for you). Get one at https://app.pinecone.io"
            )
        try:
            from pinecone import Pinecone, ServerlessSpec
        except ImportError:
            raise SystemExit(
                "pinecone not installed. Run:  pip install pinecone\n"
                "(not added to requirements.txt for you — flag for the owner.)"
            )
        self._pc = Pinecone(api_key=api_key)
        self.namespace = namespace
        existing = {ix["name"] for ix in self._pc.list_indexes()}
        if index_name not in existing:
            print(f"creating Pinecone index '{index_name}' (dim={dim}, cosine)…")
            self._pc.create_index(
                name=index_name, dimension=dim, metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        self._index = self._pc.Index(index_name)

    def write(self, doc_id: str, records: list[dict]) -> None:
        vectors = []
        for r in records:
            # Pinecone metadata must be string/number/bool/list-of-strings — no
            # nulls. Leaf chunks have parent_id=None, so drop any None-valued
            # field (its absence reads the same as null at query time).
            meta = {k: v for k, v in r["metadata"].items() if v is not None}
            meta["embedding_text"] = r["embedding_text"][:38000]
            # Stamp the embedding identity so the query side can assert it uses
            # the SAME provider/model/dim (mismatched query vectors return garbage).
            meta["provider"] = r["provider"]
            meta["model"] = r["model"]
            meta["dim"] = r["dim"]
            vectors.append({"id": r["id"], "values": r["vector"], "metadata": meta})
        # Pinecone caps batch upserts; 100 is a safe chunk size.
        for i in range(0, len(vectors), 100):
            self._index.upsert(vectors=vectors[i : i + 100], namespace=self.namespace)


def make_sink(args, dim: int) -> Sink:
    if args.sink == "jsonl":
        return JsonlSink(force=args.force)
    if args.sink == "pinecone":
        return PineconeSink(index_name=args.index, dim=dim, namespace=args.namespace)
    raise SystemExit(f"unknown sink: {args.sink}")


# ============================================================================
#  Pipeline
# ============================================================================
def load_embeddable(doc_id: str) -> list[dict]:
    """Return the child/leaf chunks of a doc that carry an embedding_text."""
    path = ENRICHED_DIR / f"{doc_id}.jsonl"
    chunks = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            c = json.loads(line)
            if c.get("chunk_type") in ("child", "leaf") and c.get("embedding_text"):
                chunks.append(c)
    return chunks


def build_record(chunk: dict, vector: list[float], embedder: Embedder) -> dict:
    meta = {k: chunk.get(k) for k in META_FIELDS}
    # section_path is a list; flatten to a breadcrumb string for metadata filters.
    meta["section_path"] = " > ".join(chunk.get("section_path") or [])
    return {
        "id": chunk["chunk_id"],
        "vector": vector,
        "provider": embedder.name,
        "model": embedder.model,
        "dim": embedder.dim,
        "metadata": meta,
        "embedding_text": chunk["embedding_text"],
    }


def embed_document(doc_id: str, embedder: Embedder, sink: Sink) -> int:
    if sink.already_done(doc_id):
        return 0
    chunks = load_embeddable(doc_id)
    if not chunks:
        return 0
    vectors = embedder.embed([c["embedding_text"] for c in chunks])
    records = [build_record(c, v, embedder) for c, v in zip(chunks, vectors)]
    sink.write(doc_id, records)
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Embed enriched_chunks/{doc_id}.jsonl into a vector store."
    )
    parser.add_argument("--all", action="store_true", help="embed all docs in enriched_chunks/")
    parser.add_argument("--doc", help="single doc id, e.g. vol1_iss1_2")
    parser.add_argument("--provider", choices=["gemini", "openrouter", "qwen"],
                        default="openrouter",
                        help="embedding model family: openrouter (openai/text-embedding-"
                             "3-small via OpenRouter, one key, no task_type — the default), "
                             "gemini (native Google API with task_type=RETRIEVAL_DOCUMENT, "
                             "needs GEMINI_API_KEY), or qwen (open weights, local)")
    parser.add_argument("--or-model", default="openai/text-embedding-3-small",
                        help="OpenRouter model id when --provider openrouter")
    parser.add_argument("--qwen-model", default="Qwen/Qwen3-Embedding-0.6B",
                        help="HF model id when --provider qwen")
    parser.add_argument("--dim", type=int, default=None,
                        help="output dimension (Matryoshka). gemini/openrouter: 768/1536/"
                             "3072 (openrouter truncates client-side), default 1536 — must "
                             "match EMBED_DIM on the query side. Qwen: <= native, default "
                             "model native.")
    parser.add_argument("--sink", choices=["jsonl", "pinecone"], default="jsonl",
                        help="where vectors go")
    parser.add_argument("--index", default="ypfs-rag", help="Pinecone index name")
    parser.add_argument("--namespace", default="", help="Pinecone namespace")
    parser.add_argument("--batch-size", type=int, default=100, help="embed batch size")
    parser.add_argument("--rpm", type=int, default=90,
                        help="requests/minute throttle for hosted providers (gemini/"
                             "openrouter); 1 request = 1 batched call. 0 disables it.")
    parser.add_argument("--force", action="store_true",
                        help="overwrite existing embeddings/{doc}.jsonl (jsonl sink only)")
    args = parser.parse_args()

    if args.doc:
        doc_ids = [args.doc]
    elif args.all:
        doc_ids = [p.stem for p in sorted(ENRICHED_DIR.glob("*.jsonl"))]
    else:
        parser.print_help()
        return

    embedder = make_embedder(args)
    sink = make_sink(args, dim=embedder.dim)
    print(f"provider={embedder.name} model={embedder.model} dim={embedder.dim} "
          f"sink={args.sink} | {len(doc_ids)} docs")

    total_vecs = 0
    total_docs = 0
    try:
        for doc_id in doc_ids:
            n = embed_document(doc_id, embedder, sink)
            if n:
                print(f"embedded {doc_id}: {n} vectors")
                total_vecs += n
                total_docs += 1
    finally:
        sink.close()

    print(f"done: {total_docs} docs | {total_vecs} vectors @ {embedder.dim}d "
          f"via {embedder.name}:{embedder.model}")


if __name__ == "__main__":
    main()
