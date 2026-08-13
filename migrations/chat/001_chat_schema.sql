-- Chat UI schema (harness/chat/): conversations, turns, prompt revisions,
-- golden pairs.
--
-- Applied by `python -m harness chat-init`, NOT by `python db.py --init`.
-- schema.sql is deliberately untouched so the existing harness, its DDL path,
-- and tests/conftest.py behave exactly as they did before this feature.
--
-- Every statement here is additive: CREATE TABLE IF NOT EXISTS / CREATE INDEX
-- IF NOT EXISTS only, no ALTER on any pre-existing table. That is what makes
-- the feature installable and removable (999_rollback.sql) without touching
-- the eval harness.
--
-- Timestamp convention matches the harness domain tables: created_at is a text
-- ISO-8601 Z string, so lexicographic order == chronological order.

-- One chat thread. `role` records which side started it ('admin' | 'user') so
-- the conversation lists stay separated per role.
CREATE TABLE IF NOT EXISTS chat_conversations (
    conversation_id text PRIMARY KEY,
    title           text NOT NULL DEFAULT '',
    role            text NOT NULL,
    created_at      text NOT NULL
);

CREATE INDEX IF NOT EXISTS chat_conversations_role_idx
    ON chat_conversations (role, created_at DESC);

-- One row per question asked. The query lives here exactly once: regenerating
-- a turn adds another `runs` row (see chat_run_links), never another turn, so
-- the transcript keeps one query with a stack of responses under it.
--
-- quoted_text is the span the person selected in an earlier response before
-- typing. It is part of the query, not an annotation — nothing anchors back
-- into the rendered answer, so there is no highlight to re-find on reload.
--
-- `stale` marks turns whose answers were produced against a now-superseded
-- earlier answer (see conversations.mark_downstream_stale). Regeneration never
-- cascades; a stale turn is flagged in the UI and left alone.
CREATE TABLE IF NOT EXISTS chat_turns (
    turn_id         text PRIMARY KEY,
    conversation_id text NOT NULL REFERENCES chat_conversations(conversation_id)
                         ON DELETE CASCADE,
    turn_index      integer NOT NULL,
    query           text NOT NULL,
    quoted_text     text,
    quoted_run_id   text REFERENCES runs(run_id) ON DELETE SET NULL,
    stale           boolean NOT NULL DEFAULT false,
    created_at      text NOT NULL,
    UNIQUE (conversation_id, turn_index)
);

CREATE INDEX IF NOT EXISTS chat_turns_conversation_idx
    ON chat_turns (conversation_id, turn_index);

-- Links an existing `runs` row to the turn it answered. A side table rather
-- than two columns on `runs`, so this migration never alters a table the
-- eval harness owns. revision_index counts up per turn: the highest one is
-- the live answer, the rest collapse into the "previous responses" accordion.
CREATE TABLE IF NOT EXISTS chat_run_links (
    run_id         text PRIMARY KEY REFERENCES runs(run_id) ON DELETE CASCADE,
    turn_id        text NOT NULL REFERENCES chat_turns(turn_id) ON DELETE CASCADE,
    revision_index integer NOT NULL DEFAULT 1,
    UNIQUE (turn_id, revision_index)
);

CREATE INDEX IF NOT EXISTS chat_run_links_turn_idx
    ON chat_run_links (turn_id, revision_index DESC);

-- A system-prompt revision the agent proposed mid-run via its admin-only
-- propose_system_prompt_revision tool. The agent only ever writes
-- status='proposed'; committing is the admin's click, which calls
-- versions.save_prompt() and fills in to_prompt_id.
CREATE TABLE IF NOT EXISTS chat_prompt_revisions (
    revision_id     text PRIMARY KEY,
    conversation_id text NOT NULL REFERENCES chat_conversations(conversation_id)
                         ON DELETE CASCADE,
    source_turn_id  text REFERENCES chat_turns(turn_id) ON DELETE SET NULL,
    source_run_id   text REFERENCES runs(run_id) ON DELETE SET NULL,
    from_prompt_id  text NOT NULL REFERENCES prompt_versions(prompt_id),
    to_prompt_id    text REFERENCES prompt_versions(prompt_id),
    proposed_text   text NOT NULL,
    rationale       text NOT NULL DEFAULT '',
    status          text NOT NULL DEFAULT 'proposed',  -- proposed | accepted | dismissed
    created_at      text NOT NULL
);

CREATE INDEX IF NOT EXISTS chat_prompt_revisions_conversation_idx
    ON chat_prompt_revisions (conversation_id, created_at);

-- A query/response pair an admin marked as a reference example. Admin-only:
-- the user-facing chat has no curation controls, so there is no "who marked
-- this" column — every row here was marked by an admin by construction.
--
-- query and answer are SNAPSHOT TEXT, not joins through run_id: this is a
-- labeled dataset row for a future LLM-as-judge, and regenerating the turn it
-- came from must never silently mutate it. run_id is kept (UNIQUE) so marking
-- is idempotent per response revision and the UI can link back.
CREATE TABLE IF NOT EXISTS chat_golden_pairs (
    golden_id       text PRIMARY KEY,
    conversation_id text NOT NULL REFERENCES chat_conversations(conversation_id)
                         ON DELETE CASCADE,
    turn_id         text NOT NULL REFERENCES chat_turns(turn_id) ON DELETE CASCADE,
    run_id          text NOT NULL UNIQUE REFERENCES runs(run_id) ON DELETE CASCADE,
    query           text NOT NULL,
    answer          text NOT NULL,
    prompt_id       text NOT NULL,
    agent_model     text NOT NULL,
    note            text NOT NULL DEFAULT '',
    created_at      text NOT NULL
);

CREATE INDEX IF NOT EXISTS chat_golden_pairs_created_idx
    ON chat_golden_pairs (created_at DESC);

CREATE INDEX IF NOT EXISTS chat_golden_pairs_prompt_idx
    ON chat_golden_pairs (prompt_id);
