-- Clean uninstall of the chat UI schema (migrations/chat/001_chat_schema.sql).
--
-- Because 001 is additive-only — it creates its own tables and never alters
-- one the eval harness owns — dropping those tables returns the database to
-- exactly its pre-chat state. Nothing in schema.sql references anything here,
-- so the harness (dashboard, runs, feedback, prompt versions, task queue)
-- keeps working with these tables gone.
--
--     psql "$DATABASE_URL" -f migrations/chat/999_rollback.sql
--
-- Destructive: this deletes every conversation, turn, proposed revision, and
-- golden pair. Prompt versions saved from accepted revisions live in
-- prompt_versions and SURVIVE — they are immutable harness rows, not chat
-- rows. The `runs` rows chat turns produced also survive; they simply stop
-- being linked to a turn.

DROP TABLE IF EXISTS chat_golden_pairs CASCADE;
DROP TABLE IF EXISTS chat_prompt_revisions CASCADE;
DROP TABLE IF EXISTS chat_run_links CASCADE;
DROP TABLE IF EXISTS chat_turns CASCADE;
DROP TABLE IF EXISTS chat_conversations CASCADE;
