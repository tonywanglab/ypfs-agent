-- Remove the rubric/judge/deterministic-check/review system; add selection-
-- based supervisor feedback. Preserves existing runs/run_samples rows.
--
-- Apply once against an existing database:
--   psql "$DATABASE_URL" -f migrations/001_remove_rubrics_add_feedback.sql
--
-- Every statement is idempotent (IF EXISTS / IF NOT EXISTS), so re-running is
-- safe. `python db.py --init` (schema.sql) never removes anything, so this
-- file is the only path that drops the old objects on a pre-existing DB.

BEGIN;

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id   text PRIMARY KEY,          -- fb_<token_hex(6)>
    run_id        text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    sample_index  integer NOT NULL,
    selected_text text NOT NULL,
    comment       text NOT NULL,
    created_at    text NOT NULL
);
CREATE INDEX IF NOT EXISTS feedback_run_idx ON feedback (run_id);

-- version_reviews references reviews, so it goes first.
DROP TABLE IF EXISTS version_reviews;
DROP TABLE IF EXISTS reviews;

-- runs: drop rubric/judge columns before dropping rubric_versions (FK).
DROP INDEX IF EXISTS runs_rubric_idx;
ALTER TABLE runs
    DROP COLUMN IF EXISTS rubric_id,
    DROP COLUMN IF EXISTS judge_model,
    DROP COLUMN IF EXISTS judgment_id,
    DROP COLUMN IF EXISTS hard_failure;

-- run_samples: drop checks/judgment artifacts (answer + trace preserved).
ALTER TABLE run_samples
    DROP COLUMN IF EXISTS checks,
    DROP COLUMN IF EXISTS judgment,
    DROP COLUMN IF EXISTS hard_failure;

DROP TABLE IF EXISTS rubric_versions;

UPDATE runs SET status = 'complete' WHERE status = 'judged';

-- Neutralize any queued/running rubric_draft tasks so a worker doesn't choke
-- on a task kind that no longer has an executor.
UPDATE tasks SET status = 'failed', error = 'rubric drafting removed', finished_at = now()
 WHERE kind = 'rubric_draft' AND status IN ('queued', 'running');

COMMIT;
