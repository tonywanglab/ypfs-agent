-- Vector store + error log schema for the YPFS agent (pgvector on Postgres).
--
-- Applied idempotently by db.init_schema() (and `python db.py --init`). The
-- {{DIM}} token is substituted with EMBED_DIM before execution, so the vector
-- column width matches the embedder the corpus was built with.

CREATE EXTENSION IF NOT EXISTS vector;

-- One row per embedded chunk (child + leaf). Mirrors the metadata Pinecone
-- stored per record; provider/model/dim is the identity stamp the query side
-- asserts so a mismatched embedder fails loud instead of returning garbage.
CREATE TABLE IF NOT EXISTS chunks (
    id             text PRIMARY KEY,        -- chunk_id
    embedding      vector({{DIM}}),
    doc_id         text,
    document_type  text,                    -- filtered at query time
    chunk_type     text,
    title          text,
    page           integer,
    parent_id      text,
    section_path   text,
    embedding_text text,
    provider       text,
    model          text,
    dim            integer
);

-- HNSW (not IVFFlat): needs no training data, so it works on an empty/small
-- table. Cosine ops to match Pinecone's cosine metric (vectors are already
-- L2-normalized on the ingestion side).
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS chunks_document_type_idx
    ON chunks (document_type);

-- One row per agent/tool runtime error, for observability. run_id groups the
-- errors emitted within a single agent.run() call.
CREATE TABLE IF NOT EXISTS agent_errors (
    id          bigserial PRIMARY KEY,
    created_at  timestamptz NOT NULL DEFAULT now(),
    run_id      text,
    error_type  text,                       -- 'tool_error' | 'api_error' | 'max_steps'
    tool_name   text,
    message     text,
    context     jsonb
);

CREATE INDEX IF NOT EXISTS agent_errors_run_id_idx
    ON agent_errors (run_id);
