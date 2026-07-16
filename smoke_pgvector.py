"""
End-to-end smoke test for the pgvector backend + error logging.

Runs against the real Postgres in DATABASE_URL (e.g. Supabase). It:
  1. creates the schema (db.init_schema)
  2. embeds a few synthetic chunks with the REAL OpenRouter embedder and upserts
     them through PgvectorSink (idempotency checked by upserting twice)
  3. runs PgvectorRetriever against a query and checks the nearest hit, the
     score conversion, metadata packing, the document_type filter, and the
     embedding-identity assertion (match + deliberate mismatch)
  4. exercises agent.errors.log_error (real insert + the no-op path)
  5. checks get_retriever()'s VECTOR_STORE routing (network-free)
  6. deletes everything it created (ids/run_id are prefixed 'smoke_')

Usage:  .venv/bin/python smoke_pgvector.py
Requires: DATABASE_URL and OPENROUTER_API_KEY in .env.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

PASS, FAIL = "PASS", "FAIL"
_results: list[tuple[str, bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    _results.append((name, bool(cond), detail))
    print(f"[{PASS if cond else FAIL}] {name}" + (f" — {detail}" if detail else ""))


SMOKE_IDS = ("smoke_1", "smoke_2", "smoke_3")
SMOKE_RUN = "smoke_run_xyz"

# (id, document_type, title, embedding_text)
SYNTH = [
    ("smoke_1", "survey", "Deposit insurance",
     "Deposit insurance reassures depositors and prevents bank runs by guaranteeing balances."),
    ("smoke_2", "case_study", "Liquidity facilities",
     "Central bank emergency liquidity facilities lend against collateral to stem funding runs."),
    ("smoke_3", "note", "Unrelated",
     "A recipe for cooking pasta: boil water, add salt, cook the noodles until al dente."),
]


def cleanup(db) -> None:
    conn = db.get_conn()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM chunks WHERE id = ANY(%s)", (list(SMOKE_IDS),))
        cur.execute("DELETE FROM agent_errors WHERE run_id = %s", (SMOKE_RUN,))


def main() -> int:
    if not os.getenv("DATABASE_URL"):
        print("DATABASE_URL not set — add it to .env (see db.py hint). Aborting.")
        return 2

    import db
    from embed_chunks import OpenRouterEmbedder, build_record, PgvectorSink

    # 1. Schema -------------------------------------------------------------
    db.init_schema(dim=1536)
    conn = db.get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT to_regclass('public.chunks'), to_regclass('public.agent_errors')")
        chunks_tbl, errors_tbl = cur.fetchone()
    check("schema: chunks + agent_errors exist", chunks_tbl is not None and errors_tbl is not None,
          f"chunks={chunks_tbl} agent_errors={errors_tbl}")

    cleanup(db)  # clear any leftovers from a prior run

    # 2. Embed + upsert through the real sink -------------------------------
    embedder = OpenRouterEmbedder(dim=1536)
    vectors = embedder.embed([s[3] for s in SYNTH])
    records = []
    for (cid, dtype, title, text), vec in zip(SYNTH, vectors):
        chunk = {"chunk_id": cid, "doc_id": "smoke_doc", "document_type": dtype,
                 "chunk_type": "leaf", "title": title, "page": 1, "parent_id": None,
                 "section_path": ["Root", title], "embedding_text": text}
        records.append(build_record(chunk, vec, embedder))

    sink = PgvectorSink(table="chunks", dim=1536)
    sink.write("smoke_doc", records)
    sink.write("smoke_doc", records)  # second write -> upsert, must not duplicate
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM chunks WHERE id = ANY(%s)", (list(SMOKE_IDS),))
        n = cur.fetchone()[0]
    check("sink: idempotent upsert (3 rows after writing twice)", n == 3, f"rows={n}")

    # 3. Retrieval ----------------------------------------------------------
    from agent.retrieval import PgvectorRetriever

    r = PgvectorRetriever()
    hits = r.retrieve("How does deposit insurance stop bank runs?", k=3, fanout=1)
    smoke_hits = [h for h in hits if h["id"] in SMOKE_IDS]
    top = smoke_hits[0] if smoke_hits else None
    check("retrieval: nearest synthetic hit is the deposit-insurance chunk",
          top is not None and top["id"] == "smoke_1",
          f"top={top['id'] if top else None}")
    check("retrieval: score is cosine similarity in [-1,1], higher=better",
          top is not None and -1.0 <= top["score"] <= 1.0 and top["score"] > 0.2,
          f"score={top['score'] if top else None:.4f}" if top else "no hit")
    check("retrieval: metadata packed, no id/distance leakage",
          top is not None and top["metadata"].get("doc_id") == "smoke_doc"
          and "id" not in top["metadata"] and "distance" not in top["metadata"],
          f"meta_keys={sorted(top['metadata']) if top else None}")

    # document_type filter
    filtered = r.retrieve("liquidity", document_type="case_study", k=5, fanout=1)
    fsmoke = [h for h in filtered if h["id"] in SMOKE_IDS]
    check("retrieval: document_type filter returns only case_study among smoke rows",
          all(h["metadata"]["document_type"] == "case_study" for h in fsmoke) and len(fsmoke) >= 1,
          f"types={[h['metadata']['document_type'] for h in fsmoke]}")

    # identity mismatch must fail loud
    r2 = PgvectorRetriever()
    class _BadEmbedder:
        name, model, dim = "openrouter", "openai/text-embedding-3-small", 768
        def embed(self, texts): return [[0.0] * 1536]  # wrong dim vs index, but row stamp says 1536
    r2._embedder = _BadEmbedder()
    try:
        r2.retrieve("deposit insurance", k=1, fanout=1)
        check("retrieval: embedding-identity mismatch raises", False, "no SystemExit raised")
    except SystemExit as e:
        check("retrieval: embedding-identity mismatch raises", "Embedding mismatch" in str(e), str(e)[:80])

    # 4. Error logging ------------------------------------------------------
    from agent import errors

    errors.log_error(SMOKE_RUN, "tool_error", "synthetic tool failure",
                     tool_name="search_corpus", context={"args": {"q": "x"}, "step": 0})
    with conn.cursor() as cur:
        cur.execute("SELECT error_type, tool_name, context FROM agent_errors WHERE run_id = %s",
                    (SMOKE_RUN,))
        rows = cur.fetchall()
    check("errors: log_error wrote one agent_errors row",
          len(rows) == 1 and rows[0][0] == "tool_error" and rows[0][1] == "search_corpus",
          f"rows={rows}")

    # no-op when DATABASE_URL is absent (must not raise, must not write)
    saved = os.environ.pop("DATABASE_URL", None)
    try:
        errors.log_error(SMOKE_RUN, "tool_error", "should be a no-op")
        noop_ok = True
    except Exception as e:  # noqa
        noop_ok = False
    finally:
        if saved is not None:
            os.environ["DATABASE_URL"] = saved
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM agent_errors WHERE run_id = %s", (SMOKE_RUN,))
        still = cur.fetchone()[0]
    check("errors: no-op without DATABASE_URL (no raise, no extra row)",
          noop_ok and still == 1, f"raised={not noop_ok} rows={still}")

    # 5. get_retriever VECTOR_STORE routing (network-free) ------------------
    import agent.retrieval as R
    orig_pc, orig_pg = R.PineconeRetriever, R.PgvectorRetriever
    R.PineconeRetriever = lambda: "PINECONE"
    R.PgvectorRetriever = lambda: "PGVECTOR"
    try:
        R._RETRIEVER = None
        os.environ.pop("VECTOR_STORE", None)
        sel_default = R.get_retriever()
        R._RETRIEVER = None
        os.environ["VECTOR_STORE"] = "pgvector"
        sel_pg = R.get_retriever()
        R._RETRIEVER = None
        os.environ["VECTOR_STORE"] = "bogus"
        try:
            R.get_retriever()
            sel_bad_raises = False
        except SystemExit:
            sel_bad_raises = True
    finally:
        R.PineconeRetriever, R.PgvectorRetriever = orig_pc, orig_pg
        R._RETRIEVER = None
        os.environ.pop("VECTOR_STORE", None)
    check("get_retriever: default=pinecone, pgvector selectable, bad value fails loud",
          sel_default == "PINECONE" and sel_pg == "PGVECTOR" and sel_bad_raises,
          f"default={sel_default} pg={sel_pg} bad_raises={sel_bad_raises}")

    # Cleanup ---------------------------------------------------------------
    cleanup(db)
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM chunks WHERE id = ANY(%s)", (list(SMOKE_IDS),))
        left = cur.fetchone()[0]
    check("cleanup: synthetic rows removed", left == 0, f"remaining={left}")

    passed = sum(1 for _, ok, _ in _results if ok)
    print(f"\n{passed}/{len(_results)} checks passed")
    return 0 if passed == len(_results) else 1


if __name__ == "__main__":
    sys.exit(main())
