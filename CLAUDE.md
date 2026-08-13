# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Agent

```bash
python -m agent          # interactive REPL (Ctrl-D to exit)
python agent/agent.py    # equivalent entry point
```

The REPL maintains conversation history across turns. `agent.run(user_msg, history, model)` returns `(answer, messages)` — `messages` is the full tool trace, usable for evals.

## Environment Variables

Required in `.env` at the repo root:

```
OPENROUTER_API_KEY=   # chat completions + embeddings (default path)
PINECONE_API_KEY=     # vector store
BEPRESS_API_TOKEN=    # metadata fetch (Phase 0 only)
```

Embedding config (query side must match ingestion side exactly — mismatch fails loud):
```
EMBED_PROVIDER=openrouter          # gemini | openrouter
EMBED_MODEL=openai/text-embedding-3-small
EMBED_DIM=1536
PINECONE_INDEX=ypfs-rag
AGENT_MODEL=anthropic/claude-sonnet-4-6   # override default model
```

Chat UI (`harness/chat/`, optional):
```
HARNESS_ADMIN_PASSWORD=   # unset ⇒ admin role disabled entirely; chat runs user-only
HARNESS_SECRET_KEY=       # optional; unset ⇒ random per process (sessions drop on restart)
```

## Ingestion Pipeline (one-time, run in order)

```bash
python fetch_metadata.py --fetch                     # Phase 0: metadata → metadata/
python pdf_to_markdown.py --all                      # Phase 1a: PDFs → markdown/
python annotate_figures.py --all                     # Phase 1b: insert [FIGURE] markers
./run_pipeline.sh                                    # shortcut for Phase 1a + 1b together
python chunk_documents.py --all                      # Phase 2: section-aware chunking → chunks/
python enrich_chunks.py --all                        # Phase 3a: add embedding_text → enriched_chunks/
python enrich_chunks.py --all --no-llm               # Phase 3a: skip LLM table summaries
python embed_chunks.py --all --sink pinecone         # Phase 3b: embed + upsert to Pinecone
python embed_chunks.py --all --sink jsonl            # Phase 3b: embed to embeddings/ (local)
python embed_chunks.py --all --provider gemini --sink jsonl
```

Per-doc variants: replace `--all` with `--doc vol1_iss1_2`. Add `--force` to overwrite.

## Architecture

### Two-sided design: ingestion vs. query

The pipeline has a hard split. **Ingestion** (repo root scripts) builds the corpus; **query** (`agent/`) uses it. The embedding provider/model/dim must be identical on both sides — every Pinecone record is stamped with `provider/model/dim` and the retriever asserts this on the first hit.

### Agent loop (`agent/agent.py`)

`run()` is the entire agent: it sends `[system] + history + [user]` to OpenRouter, appends tool calls and their results, and loops until the model produces a final answer (no tool calls) or hits `MAX_STEPS=10`. The model slug is never hardcoded into the loop — pass `model=` to `run()` to override.

`tools=` / `dispatch_fn=` extend the toolset for one run without touching the module-level registry (they default to `tools.TOOLS` / `tools.dispatch`, so omitting them is exactly the historical behavior). This is the seam `harness/chat/` uses to give admin conversations their prompt-revision tool.

### Tool registry (`agent/tools.py`)

`@tool(schema)` registers both the OpenAI function-call schema (sent to the model each turn in `TOOLS`) and the Python implementation (in `_FNS`). `dispatch(name, args)` runs one tool call and swallows all exceptions — bad tool calls become error dicts the model can read and recover from, rather than crashing the loop.

Two tools are live:
- **`search_corpus`** — embeds the query, retrieves from Pinecone, expands child hits to their parent section, deduplicates by section key. Falls back to Pinecone's `embedding_text` field when `chunks/` is absent on disk.
- **`get_document`** — reads `metadata/{doc_id}.json` + `markdown/{doc_id}.md`; includes a path-traversal guard.

### Chunking scheme (`chunk_documents.py`)

Documents are split at markdown headers. Sections ≤ 300 tokens → single **leaf** chunk (embedded). Sections > 300 tokens → one **parent** chunk (full text, never embedded) + **child** chunks (~150 tokens, one-paragraph overlap, embedded). Only children and leaves go to Pinecone; retrieval fetches the parent section for context. Every chunk carries `section_path`, `doc_id`, `document_type`, `title`, `page`, and `figure_refs`.

### Source hierarchy (system prompt)

The agent treats document types with a strict trust order: **surveys** (highest — shape reasoning, never cite directly) → **lessons_learned** (opinions, cross-sector) → **case_studies** (cite these for design suggestions) → **articles/notes** (primary sources, cite on demand).

### Chat UI (`harness/chat/`)

An opt-in feature package, deliberately isolated. Its DDL is `migrations/chat/001_chat_schema.sql`
(applied by `python -m harness chat-init`, **not** by `db.py --init`); `schema.sql` is untouched.
The DDL is additive only — no `ALTER` on any existing table, and a `chat_run_links` side table
carries the run↔turn link instead of adding columns to `runs`. Routes are a Flask blueprint
registered in one line from `create_app()`.

Key invariants when working here:

- **A turn owns the query; a run owns an answer.** Regenerating adds a `runs` row at
  `revision_index + 1` on the same turn, never a second turn. `conversations.history_for()` replays
  only each turn's *active* revision, so a superseded answer never re-enters the model's context and
  the question appears exactly once.
- **`compose_message(turn)` is the single renderer** of a turn's model-visible text (quoted span as
  a blockquote + typed query). Used by both the live run and history replay — never build that text
  anywhere else, or the model sees two versions of one turn.
- **A quoted span is part of the question**, not an annotation. Nothing anchors back into a rendered
  answer, which is why there is no highlight layer or re-anchoring code.
- **The admin tool gate is absence from the schema list**, not a runtime check: `admin_tools.agent_kwargs()`
  returns `tools=[*TOOLS, SCHEMA]` plus a `dispatch_fn`, and user runs pass neither. Never mutate
  `agent.tools.TOOLS` — it would leak the tool into every run in the process.
- **The agent proposes, the admin commits.** `propose_system_prompt_revision` only ever writes
  `status='proposed'`; `revisions.accept()` is the only path to `versions.save_prompt()`.
- **Auth is default-deny.** `auth.USER_ENDPOINTS` lists what an anonymous user may reach; a new
  route is admin-only unless added there. Golden pairs are admin-only.

### Evals (`agent/evals.py`)

`Case` dataclass pairs a `user_msg` with a `Check: (answer, messages) -> bool`. Because `run()` returns the full tool trace, checks can assert on tool invocation patterns, not just the final answer. `run_evals` is a stub — implement the loop there.
