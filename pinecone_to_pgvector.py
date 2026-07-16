"""
Transfer embedded vectors from Pinecone into pgvector — no re-embedding.

Every Pinecone record already carries its vector plus the metadata the `chunks`
table needs (doc_id, document_type, chunk_type, title, page, parent_id,
section_path, embedding_text, and the provider/model/dim identity stamp), so
this just copies records across stores. Vectors are reused verbatim, so the
pgvector corpus is bit-for-bit the same embeddings as Pinecone.

Reuses PgvectorSink (idempotent upsert by id) so re-running is safe.

Usage:
  python pinecone_to_pgvector.py --doc vol1_iss1_1     # one document (id prefix)
  python pinecone_to_pgvector.py --all                 # the whole index

Requires PINECONE_API_KEY (source) and DATABASE_URL (sink) in .env.
"""

import argparse
import os

from dotenv import load_dotenv

load_dotenv()

from embed_chunks import PgvectorSink  # reuse the idempotent upsert sink

# Metadata fields → chunks columns (same set embed_chunks wrote to Pinecone).
_META_FIELDS = ("doc_id", "document_type", "chunk_type", "title", "page", "parent_id")


def _vid(item) -> str:
    """idx.list() yields ListItem objects (or plain id strings)."""
    return item.id if hasattr(item, "id") else item


def _iter_ids(idx, namespace: str, prefix: str | None):
    # idx.list() pages vary by SDK version: a ListResponse (with a .vectors list
    # of ListItem), a plain list of ids/ListItems, or a single id. Handle all.
    for page in idx.list(namespace=namespace, prefix=prefix):
        items = getattr(page, "vectors", None)
        if items is None:
            items = page if isinstance(page, (list, tuple)) else [page]
        for item in items:
            yield _vid(item)


def _to_record(vid: str, values, md: dict) -> dict:
    """Shape a Pinecone record into PgvectorSink's expected record dict."""
    meta = {k: md.get(k) for k in _META_FIELDS}
    meta["section_path"] = md.get("section_path")
    return {
        "id": vid,
        "vector": list(values),
        "provider": md.get("provider"),
        "model": md.get("model"),
        "dim": int(md["dim"]) if md.get("dim") is not None else len(values),
        "metadata": meta,
        "embedding_text": md.get("embedding_text", ""),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Copy vectors from Pinecone into pgvector.")
    ap.add_argument("--doc", help="single doc id (matched as the id prefix, e.g. vol1_iss1_1)")
    ap.add_argument("--all", action="store_true", help="transfer the entire index")
    ap.add_argument("--table", default="chunks", help="pgvector table name")
    ap.add_argument("--batch", type=int, default=100, help="fetch/upsert batch size")
    args = ap.parse_args()
    if not args.doc and not args.all:
        ap.error("pass --doc <id> or --all")

    from pinecone import Pinecone

    index_name = os.getenv("PINECONE_INDEX", "ypfs-rag")
    namespace = os.getenv("PINECONE_NAMESPACE", "")
    idx = Pinecone(api_key=os.environ["PINECONE_API_KEY"]).Index(index_name)
    prefix = f"{args.doc}_" if args.doc else None

    sink = PgvectorSink(table=args.table, dim=int(os.getenv("EMBED_DIM", "1536")))
    print(f"source: pinecone '{index_name}' (ns={namespace!r}) | sink: pgvector '{args.table}' "
          f"| scope: {args.doc or 'ALL'}")

    total = 0
    buf: list[str] = []

    def flush() -> None:
        nonlocal total, buf
        if not buf:
            return
        fetched = idx.fetch(ids=buf, namespace=namespace)
        records = [_to_record(vid, v.values, dict(v.metadata or {}))
                   for vid, v in fetched.vectors.items()]
        sink.write(args.doc or "all", records)
        total += len(records)
        print(f"  transferred {total} vectors…")
        buf = []

    for vid in _iter_ids(idx, namespace, prefix):
        buf.append(vid)
        if len(buf) >= args.batch:
            flush()
    flush()

    print(f"done: {total} vectors → pgvector '{args.table}'")


if __name__ == "__main__":
    main()
