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

-- ---------------------------------------------------------------------------
-- Evaluation harness (harness/): cases, prompt versions, runs, feedback,
-- task queue.
--
-- Timestamp convention: domain tables store created_at/used_at as text
-- ISO-8601 Z strings — exactly what the harness dataclasses carry, and
-- lexicographic order == chronological order. The `tasks` table alone uses
-- timestamptz because the stale-claim reaper does interval arithmetic on it.
-- ---------------------------------------------------------------------------

-- Eval test-case definitions. adhoc=true marks chat-launched one-off cases,
-- hidden from the seeded-case pickers.
CREATE TABLE IF NOT EXISTS cases (
    case_id    text PRIMARY KEY,
    prompt     text NOT NULL,
    tags       jsonb NOT NULL DEFAULT '[]',
    notes      text NOT NULL DEFAULT '',
    adhoc      boolean NOT NULL DEFAULT false,
    created_at text NOT NULL
);

-- Immutable system-prompt versions ('prompt_v{N}'). UNIQUE(version) enforces
-- the append-only max+1 allocation under concurrent writers.
CREATE TABLE IF NOT EXISTS prompt_versions (
    prompt_id        text PRIMARY KEY,
    version          integer NOT NULL UNIQUE,
    text             text NOT NULL,
    created_at       text NOT NULL,
    parent_prompt_id text REFERENCES prompt_versions(prompt_id),
    rationale        text NOT NULL DEFAULT ''
);

-- One row per eval run. Inserted at run start (status='pending') so a crashed
-- run stays inspectable; finalized to 'complete'. case_snapshot is the
-- immutable copy of the case as it was when the run launched.
CREATE TABLE IF NOT EXISTS runs (
    run_id        text PRIMARY KEY,
    case_id       text NOT NULL REFERENCES cases(case_id),
    case_snapshot jsonb NOT NULL,
    prompt_id     text NOT NULL REFERENCES prompt_versions(prompt_id),
    agent_model   text NOT NULL,
    status        text NOT NULL DEFAULT 'pending',   -- pending | complete
    sample_count  integer NOT NULL DEFAULT 1,
    created_at    text NOT NULL
);
CREATE INDEX IF NOT EXISTS runs_prompt_idx  ON runs (prompt_id);
CREATE INDEX IF NOT EXISTS runs_created_idx ON runs (created_at);

-- Per-sample artifacts (answer + tool trace).
CREATE TABLE IF NOT EXISTS run_samples (
    run_id       text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    sample_index integer NOT NULL,
    answer       text NOT NULL,
    trace        jsonb NOT NULL,
    PRIMARY KEY (run_id, sample_index)
);

-- Selection-based supervisor feedback on a run sample's answer. Accumulates
-- per run; a run's full feedback list is sent to the LLM at once to draft a
-- revised system prompt (see harness/versions.py:draft_prompt).
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id   text PRIMARY KEY,          -- fb_<token_hex(6)>
    run_id        text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    sample_index  integer NOT NULL,
    selected_text text NOT NULL,
    comment       text NOT NULL,
    created_at    text NOT NULL
);
CREATE INDEX IF NOT EXISTS feedback_run_idx ON feedback (run_id);

-- Work queue for background tasks (experiment runs + prompt drafts).
-- Workers claim rows with a single atomic UPDATE ... FOR UPDATE SKIP LOCKED
-- and bump heartbeat_at while executing; the reaper requeues stale claims.
CREATE TABLE IF NOT EXISTS tasks (
    task_id      text PRIMARY KEY,
    kind         text NOT NULL,                  -- experiment | prompt_draft
    status       text NOT NULL DEFAULT 'queued', -- queued | running | finished | failed
    payload      jsonb NOT NULL,
    progress     jsonb NOT NULL DEFAULT '{}',
    result       jsonb,
    run_id       text REFERENCES runs(run_id) ON DELETE SET NULL,
    error        text,
    attempts     integer NOT NULL DEFAULT 0,
    claimed_by   text,
    claimed_at   timestamptz,
    heartbeat_at timestamptz,
    created_at   timestamptz NOT NULL DEFAULT now(),
    finished_at  timestamptz
);
CREATE INDEX IF NOT EXISTS tasks_claim_idx ON tasks (status, created_at);
