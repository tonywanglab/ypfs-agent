# Yale Program on Financial Stability — RAG Pipeline
Authors: Rifat Tarafder and Tony Wang

## Overview

An agentic RAG pipeline giving frontier models access to the full YPFS Journal of Financial Crises corpus (~588 documents spanning articles, case studies, surveys, lessons-learned interviews, and archive notes). The goal is a read-only financial crisis analyst agent that retrieves and reasons over the corpus to produce decision-useful analysis for central bankers, regulators, and finance ministry staff.

## Ingestion Pipeline

The pipeline runs in phases, each building on the previous:

**Phase 0 — Metadata fetch** (`fetch_metadata.py`)
Queries the bepress Digital Commons Content-Out API for all Journal of Financial Crises records, normalizes each record (title, authors, abstract, document type, volume/issue), and writes one JSON file per document to `metadata/` plus a flat `metadata/index.json` for fast lookup. Run this once before anything else.

```bash
python fetch_metadata.py --fetch
```

**Phase 1a — PDF to Markdown** (`pdf_to_markdown.py`)
Converts each PDF in `pdfs/` to Markdown using `pymupdf4llm`, skipping the first two pages of EliScholar boilerplate. Extracts embedded images as PNGs into `assets/{doc_id}/`. Junk images (decorative rules, icon slivers) are filtered out immediately via `figure_filters.py`. Output goes to `markdown/{doc_id}.md`.

```bash
python pdf_to_markdown.py --all
```

**Phase 1b — Figure annotation** (`annotate_figures.py`)
Post-processes the raw markdown to insert structured `[FIGURE id=... type=... page=... label="..." file=... caption="..."]` markers. Handles three layout patterns (caption-before-image, image-before-caption, captions buried in OCR blocks), classifies each exhibit as `table`, `chart`, `diagram`, or `figure`, and renames image files to match their label. These markers are what will make figures addressable by the agent's `list_exhibits` / `get_figure` tools.

```bash
python annotate_figures.py --all
```

**Run both Phase 1 steps at once:**

```bash
./run_pipeline.sh
```

**Phase 2 — Chunking** (`chunk_documents.py`)
Splits each `markdown/{doc_id}.md` into RAG-ready chunks, writing one JSON-lines file per document to `chunks/{doc_id}.jsonl`. Chunking is section-aware: the document is first split at every markdown header, then each section is routed by token count:

- **Sections ≤ 300 tokens** become a single **leaf** chunk, embedded directly.
- **Sections > 300 tokens** become a **parent** chunk holding the full section text (fetched by ID at query time, never embedded) plus a set of **child** chunks (~150 tokens each, split on paragraph boundaries with one-paragraph overlap) that are embedded.

Only child and leaf chunks go into the vector store; when a child is retrieved, its `parent_id` is used to pull the full section text for the model. Every chunk carries its `section_path` breadcrumb (prepended to leaf/child text so embeddings capture document location), `doc_id`, `document_type`, `title`, `token_count`, `page`, and `figure_refs` (IDs of any `[FIGURE]` markers in the chunk). Token counts use `tiktoken` (gpt-4o encoding).

```bash
python chunk_documents.py --all
python chunk_documents.py --doc vol1_iss1_2
python chunk_documents.py --all --force   # overwrite existing chunk files
```

Current output: 66,437 chunks across 588 documents (6,267 leaf, 7,258 parent, 52,912 child).

**Phase 3a — Chunk enrichment** (`enrich_chunks.py`)
Reads each `chunks/{doc_id}.jsonl` file and adds an `embedding_text` field to every `child` and `leaf` chunk. The enriched text wraps the original prose with four retrieval signals: (1) document title, (2) section breadcrumb (already in chunk text), (3) verbatim figure/table-image captions pulled from the `[FIGURE]` markers in `markdown/`, and (4) 1–2 sentence LLM summaries of any inline markdown pipe tables. The original `text` field is preserved byte-for-byte; enrichment is additive only. Output goes to `enriched_chunks/{doc_id}.jsonl`. A table-summary cache at `enriched_chunks/.table_summary_cache.json` makes re-runs free for duplicate tables.

LLM calls use OpenRouter (`OR_API_KEY`), defaulting to `anthropic/claude-haiku-4-5`. Use `--no-llm` to skip table summaries entirely (captions only, zero API calls).

```bash
python enrich_chunks.py --all
python enrich_chunks.py --doc vol1_iss1_2
python enrich_chunks.py --all --force          # overwrite existing enriched files
python enrich_chunks.py --all --no-llm         # captions only, no LLM calls
python enrich_chunks.py --doc X --model anthropic/claude-haiku-4-5
```

Corpus scale: 588 docs → 59,179 embeddable chunks with `embedding_text`.

**Phase 3b — Embedding** (`embed_chunks.py`)
Reads `enriched_chunks/{doc_id}.jsonl`, embeds the `embedding_text` of every `child` and `leaf` chunk, and writes vectors to a configurable sink. The step is model-agnostic and store-agnostic:

- **Embedders:** `OpenRouterEmbedder` (default — `openai/text-embedding-3-small` @ 1536d via OpenRouter, one `OR_API_KEY` for both chat and embeddings), `GeminiEmbedder` (native `gemini-embedding-001`, adds `task_type=RETRIEVAL_DOCUMENT`, requires `GEMINI_API_KEY`), or `QwenEmbedder` (open weights, local via `sentence-transformers`). Every output record stores `provider/model/dim` so vectors are reproducible and never mixed. All vectors are L2-normalized before storage. Default dim is 1536 (Matryoshka truncation) to halve storage versus native 3072.
- **Sinks:** `JsonlSink` (portable, free, resumable — writes to `embeddings/{doc_id}.jsonl`) or `PineconeSink` (auto-creates a cosine index, idempotent upsert by chunk id, requires `PINECONE_API_KEY`).
- The query side (`harness/retrieval.py`) must embed with the SAME provider/model/dim — set via `EMBED_PROVIDER` / `EMBED_MODEL` / `EMBED_DIM`. Defaults on both sides agree, and a mismatch fails loud. The OpenRouter path is symmetric (no `task_type`); Gemini is asymmetric (`RETRIEVAL_DOCUMENT` ingest, `RETRIEVAL_QUERY` query).

```bash
python embed_chunks.py --all --sink jsonl                 # default: openrouter / openai/text-embedding-3-small
python embed_chunks.py --all --sink pinecone
python embed_chunks.py --all --provider gemini --sink jsonl
python embed_chunks.py --all --provider qwen   --sink jsonl
python embed_chunks.py --doc vol1_iss1_2 --sink jsonl
python embed_chunks.py --all --force                      # overwrite existing embeddings
```

Corpus cost estimate (`text-embedding-3-small`, 59k chunks, ~8.1M tokens): ~$0.16. Fits Pinecone free tier comfortably (59k records << 300k cap; ~0.5 GB at 1536-dim << 2 GB cap).

**Phase 4 — Retrieval & agent** (`harness/retrieval.py`, `agent/agent.py`)
The query side of the RAG loop, now wired end-to-end. `harness/retrieval.py` embeds a user query with the **same** provider/model/dim the corpus was built with (default OpenRouter / `openai/text-embedding-3-small` / 1536d), runs a Pinecone nearest-neighbor query with an optional `document_type` filter, and asserts the index's stamped embedding identity matches the query embedder — a mismatch fails loud rather than returning garbage. `search_knowledge_base` then expands each child/leaf hit to its full **parent section** and dedupes, so the model gets the precision of a child match with the context of a whole section. `agent/agent.py` is a REPL that runs a frontier model (default `anthropic/claude-sonnet-4.6` via OpenRouter) through the harness tool loop.

```bash
# .env (query side must match the ingestion side; these are also the code defaults)
EMBED_PROVIDER=openrouter
EMBED_MODEL=openai/text-embedding-3-small
EMBED_DIM=1536

python agent/agent.py            # interactive REPL over the corpus
```

## Subdirectories

### `pdfs/`
Raw PDF downloads of every Journal of Financial Crises document (~588 files), named by `doc_id` (e.g. `vol1_iss1_2.pdf`).

### `metadata/`
One JSON file per document produced by Phase 0. Each file contains the normalized record (doc_id, document_type, title, authors, abstract, keywords, publication date, URL, volume/issue). `index.json` is a flat lookup table over all records, keyed by doc_id.

### `markdown/` (generated)
Markdown conversions of every PDF produced by Phase 1a+1b. Each file contains the document text with `[FIGURE]` markers inserted at every exhibit location, and inline image references pointing to `assets/{doc_id}/`.

### `assets/` (generated)
Extracted PNG images, one subdirectory per document (`assets/{doc_id}/`). Only non-junk figures survive here (real charts, diagrams, tables as images).

### `chunks/` (generated)
JSON-lines chunk files produced by Phase 2, one per document (`chunks/{doc_id}.jsonl`). Each line is a single chunk with its `chunk_id`, `parent_id`, `chunk_type` (`leaf` | `parent` | `child`), text, and metadata. These feed the enrichment/embedding phase.

### `enriched_chunks/` (generated)
JSON-lines files produced by Phase 3a, one per document (`enriched_chunks/{doc_id}.jsonl`). Mirrors `chunks/` exactly, with an `embedding_text` field added to every `child` and `leaf` chunk. A hidden `.table_summary_cache.json` file persists LLM table summaries keyed by table hash to avoid redundant API calls across runs.

### `embeddings/` (generated by Phase 3b — jsonl sink)
One JSON-lines file per document (`embeddings/{doc_id}.jsonl`), each line a vector record with `chunk_id`, `embedding` (float list), `provider`, `model`, and `dim`. Only written when using `--sink jsonl`; the Pinecone sink upserts directly to the index instead.

### `text/`
Plain-text extractions of the corpus documents.

### `harness/`
The agent harness — defines what the assistant is, independent of the retrieval backend.
- `AGENTS.md` — system prompt: identity, hard constraints (read-only, no fabrication), tool API, source hierarchy (surveys > case studies > lessons-learned > articles > notes), and behavioral method.
- `corpus_exhibit_tools.py` — the agent's tool implementations. **Retrieval tools are live:** `search_knowledge_base` (Pinecone vector search with child-match → parent-section expansion), `get_document`, `list_exhibits`, `load_skill`, and `analyze_data` (`describe` / `pct_change` / `peak_trough`). Exhibit-extraction tools (`get_table`, `get_figure`, `extract_chart_data`, `describe_diagram`) are still stubs that return `not_available` and point the model back to `get_document`. All read-only.
- `retrieval.py` — the **query-side embedding seam**. Reuses `embed_chunks.py`'s embedder classes to embed a query with the SAME provider/model/dim as the corpus, queries Pinecone, and asserts the index's stamped `provider/model/dim` matches (fails loud otherwise). Configured by `EMBED_PROVIDER` / `EMBED_MODEL` / `EMBED_DIM` / `PINECONE_INDEX` / `PINECONE_NAMESPACE`.
- `SKILL_crisis_analysis.md` — pageable skill with the full diagnostic and response framework (liquidity vs. solvency, run detection, contagion mapping, Bagehot-plus toolkit). Loaded on demand via `load_skill("crisis-analysis")`.
- `SKILL_evidence_synthesis.md` — pageable skill for cross-source citation, trust weighting, and conflict resolution.

### `agent/`
The runnable agent. `agent.py` is a REPL that drives a frontier model (default `anthropic/claude-sonnet-4.6` via OpenRouter) through the `harness/` tool loop: it sends the tool schemas, executes tool calls against `corpus_exhibit_tools.py`, and loops until the model produces a final answer. Saved transcripts land in `agent/responses/`.

### `benchmarking/`
Benchmark harness and outputs for evaluating frontier model performance on corpus questions prior to building the RAG pipeline.

## Utility Scripts

| File | Purpose |
|---|---|
| `figure_filters.py` | Shared library: junk-image detection, OCR block stripping, unreferenced PNG cleanup. Imported by `pdf_to_markdown.py` and `annotate_figures.py`. |
| `test_ocr_quality.py` | Audits converted docs: counts junk images, leftover OCR blocks, and `[FIGURE]` markers per document. |
| `validate_junk_filter.py` | Regression test: re-converts a fixed set of known-tricky docs and asserts zero junk images survive in the output. |
| `bsscrape.py` | Scraper for downloading the PDF corpus. |
| `chunk_documents.py` | Phase 2 chunker: splits `markdown/` docs into section-aware parent/child/leaf chunks in `chunks/`. |
| `enrich_chunks.py` | Phase 3a: adds `embedding_text` to every child/leaf chunk (document title + captions + LLM table summaries); writes to `enriched_chunks/`. |
| `embed_chunks.py` | Phase 3b: embeds `embedding_text` via OpenRouter (default), Gemini, or Qwen and writes vectors to `embeddings/` (jsonl) or a Pinecone index. |
| `harness/retrieval.py` | Phase 4 query side: embeds a query with the corpus's provider/model/dim and returns nearest Pinecone matches; asserts embedding identity. |
| `agent/agent.py` | Phase 4 agent: REPL that drives a frontier model through the `harness/` tool loop (semantic search, document/skill retrieval, analysis). |
