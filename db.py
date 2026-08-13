"""
Postgres + pgvector connection seam.

Shared by the ingestion side (`embed_chunks.py` PgvectorSink), the query side
(`agent/retrieval.py` PgvectorRetriever), and the error logger
(`agent/errors.py`). One process-level connection, mirroring the retriever
singleton — open it once, reuse it everywhere.

The connection is opened from DATABASE_URL. For a hosted Postgres
(Supabase/Neon/RDS) put `sslmode=require` in the URL. `prepare_threshold=None`
keeps the connection safe behind a transaction-mode pooler (Supabase :6543 /
PgBouncer), which rejects the prepared statements psycopg would otherwise cache.

Schema lives in `schema.sql`; `init_schema()` applies it idempotently and is
also runnable directly:  python db.py --init
"""

import os
import threading
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
DEFAULT_DIM = 1536

# Process-level singleton: one Postgres connection per process.
_CONN = None

# Per-thread connections for concurrent callers (web threads + queue workers).
# A psycopg connection is not safe for concurrent use, so each thread gets its
# own, opened with the same pooler-safe settings as get_conn().
_THREAD_LOCAL = threading.local()


def _require_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise SystemExit(
            "DATABASE_URL not set. Add it to .env, e.g.\n"
            "  DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require\n"
            "For a hosted/pooled Postgres (Supabase/Neon/RDS) include sslmode=require."
        )
    return url


def get_conn():
    """Return the process-level psycopg connection, opening it on first use.

    The pgvector type adapter is registered so callers can pass/receive Python
    lists as `vector` values. The `vector` extension must exist before the
    adapter can resolve its type OID, so we ensure it (guarded by a privilege-
    safe existence check) before registering.
    """
    global _CONN
    if _CONN is not None and not _CONN.closed:
        return _CONN
    _CONN = _connect()
    return _CONN


def _connect():
    try:
        import psycopg
        from pgvector.psycopg import register_vector
    except ImportError:
        raise SystemExit(
            "psycopg/pgvector not installed. Run:\n"
            "  pip install 'psycopg[binary]' pgvector"
        )

    # autocommit: upserts and error rows land without an explicit commit from
    # every caller. prepare_threshold=None: no prepared statements, so this is
    # safe behind a transaction-mode pooler.
    conn = psycopg.connect(_require_url(), autocommit=True, prepare_threshold=None)

    # register_vector resolves the `vector` type OID, which requires the
    # extension to already exist. Only attempt CREATE when it's absent, so an
    # app user without CREATE EXTENSION privilege still works against a DB where
    # an admin pre-installed it (common on hosted Postgres).
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        if cur.fetchone() is None:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    return conn


def get_thread_conn():
    """Return this thread's psycopg connection, opening it on first use.

    Same settings as get_conn() (autocommit, no prepared statements, pgvector
    adapter) but one connection per thread, so queue workers and web threads
    can query concurrently. Reconnects if the connection was closed or died.
    """
    conn = getattr(_THREAD_LOCAL, "conn", None)
    if conn is not None and not conn.closed:
        return conn
    conn = _connect()
    _THREAD_LOCAL.conn = conn
    return conn


def to_vector(values):
    """Wrap a list of floats as a pgvector Vector.

    A plain Python list would be dumped as a Postgres array; the Vector wrapper
    is what register_vector's dumper turns into a `vector` literal. Used on both
    the insert (PgvectorSink) and query (PgvectorRetriever) sides.
    """
    from pgvector import Vector
    return Vector(values)


def init_schema(dim: int | None = None) -> None:
    """Apply schema.sql idempotently (extension + tables + indexes).

    `dim` sets the vector column width; it defaults to EMBED_DIM (or 1536) and
    only takes effect when the `chunks` table is first created.
    """
    dim = dim or int(os.getenv("EMBED_DIM", str(DEFAULT_DIM)))
    ddl = SCHEMA_PATH.read_text().replace("{{DIM}}", str(dim))
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(ddl)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="YPFS Postgres/pgvector schema tool.")
    parser.add_argument("--init", action="store_true",
                        help="create the vector extension, chunks + agent_errors tables, and indexes")
    args = parser.parse_args()

    if args.init:
        init_schema()
        host = (os.getenv("DATABASE_URL", "").split("@")[-1] or "?").split("?")[0]
        print(f"schema applied (dim={os.getenv('EMBED_DIM', DEFAULT_DIM)}) → {host}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
