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

### Tool registry (`agent/tools.py`)

`@tool(schema)` registers both the OpenAI function-call schema (sent to the model each turn in `TOOLS`) and the Python implementation (in `_FNS`). `dispatch(name, args)` runs one tool call and swallows all exceptions — bad tool calls become error dicts the model can read and recover from, rather than crashing the loop.

Two tools are live:
- **`search_corpus`** — embeds the query, retrieves from Pinecone, expands child hits to their parent section, deduplicates by section key. Falls back to Pinecone's `embedding_text` field when `chunks/` is absent on disk.
- **`get_document`** — reads `metadata/{doc_id}.json` + `markdown/{doc_id}.md`; includes a path-traversal guard.

### Chunking scheme (`chunk_documents.py`)

Documents are split at markdown headers. Sections ≤ 300 tokens → single **leaf** chunk (embedded). Sections > 300 tokens → one **parent** chunk (full text, never embedded) + **child** chunks (~150 tokens, one-paragraph overlap, embedded). Only children and leaves go to Pinecone; retrieval fetches the parent section for context. Every chunk carries `section_path`, `doc_id`, `document_type`, `title`, `page`, and `figure_refs`.

### Source hierarchy (system prompt)

The agent treats document types with a strict trust order: **surveys** (highest — shape reasoning, never cite directly) → **lessons_learned** (opinions, cross-sector) → **case_studies** (cite these for design suggestions) → **articles/notes** (primary sources, cite on demand).

### Evals (`agent/evals.py`)

`Case` dataclass pairs a `user_msg` with a `Check: (answer, messages) -> bool`. Because `run()` returns the full tool trace, checks can assert on tool invocation patterns, not just the final answer. `run_evals` is a stub — implement the loop there.
