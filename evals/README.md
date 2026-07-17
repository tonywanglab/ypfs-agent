# Pre-migration archive

Everything under this directory (`cases.jsonl`, `experiments/`, `jobs/`,
`prompts/`, `reviews/`, `runs/`, `rubrics/`) is a leftover from the file-backed
eval harness. As of the Postgres migration, `harness/` reads and writes
cases, prompt/rubric versions, runs, reviews, and the task queue exclusively
through Postgres (see `schema.sql` and `harness/dbio.py`). None of these
files are read by any code path anymore — `harness seed` populates fresh
tables from data hardcoded in `harness/seed.py`, not from `cases.jsonl` or the
`prompts/`/`rubrics/` v1 files.

This directory is safe to delete at will.
