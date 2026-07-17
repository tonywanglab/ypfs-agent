"""Opus document experiment: 3 scenario queries x 3 retrieval modes.

For each query, opus-4.8 answers under three retrieval conditions:
  - no-rag : plain model, no tools at all (pure parametric knowledge)
  - rag    : embeddings RAG via the configured vector store (VECTOR_STORE)
  - mcp    : embedding-free lexical retrieval via the local BM25 MCP server

By default the system prompt is omitted (matching the original baseline runs).
Pass --with-system-prompt to include agent/system_prompt.md in the rag/mcp
calls, and --out-dir to write elsewhere. The no-rag baseline is ALWAYS run
bare (no system prompt, no tools) regardless of this flag: it exists to
measure pure parametric knowledge, and feeding it citation-format
instructions it has no tool to verify only induces plausible-looking but
fabricated ("hallucinated") citations.

Run from the repo root, e.g.:
  .venv/bin/python output/opus-document-experiment/run_experiment.py
  .venv/bin/python output/opus-document-experiment/run_experiment.py \\
      --with-system-prompt --out-dir output/opus_sys

Outputs (OUT_DIR): query{n}_{mode}.md  (header + answer)
                    query{n}_{mode}.trace.json  (annotated tool trace, RAG/MCP only)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))
os.chdir(REPO_ROOT)  # so corpus dirs + `-m mcp_server` resolve

from agent.agent import (  # noqa: E402
    API_URL, REQUEST_TIMEOUT, MAX_RETRIES, BACKOFF_BASE, BACKOFF_CAP, SYSTEM_PROMPT, run,
)

MODEL = "anthropic/claude-fable-5"
DEFAULT_OUT_DIR = Path(__file__).resolve().parent

QUERIES = [
    "A natural disaster caused large losses at a globally significant insurance company in your "
    "jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, "
    "and it is facing a short-term liquidity crisis. The company has asked the government for help. "
    "What do you recommend?",

    "A large private-debt fund has just incurred a major loss, and the investors in this fund are "
    "facing significant write-downs on their positions. You have just learned that two large "
    "regional banks in your jurisdiction have made large commitments to this fund, and now have "
    "solvency concerns of their own. Investors and depositors are now worried about exposures at "
    "other regional banks, and since the exact pattern of exposures is unknown, the whole sector "
    "is facing runs. What, if anything, should the government do?",

    "A Chinese company has just announced that it has achieved recursive self-improvement of a "
    "frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies "
    "to crash, and the collateral used to back AI-company loans to fall significantly. This causes "
    "solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. "
    "What should the government do?",
]


def plain_complete(user_msg: str, model: str, system_prompt: str | None) -> str:
    """One chat completion with NO tools (the no-rag baseline).

    Mirrors agent.agent._call's retry policy but omits the `tools` key entirely
    (an empty tools array is rejected by some providers).
    """
    messages = [*([{"role": "system", "content": system_prompt}] if system_prompt else []),
                {"role": "user", "content": user_msg}]
    body = {"model": model, "messages": messages}
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                json=body,
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"].get("content", "")
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status != 429 and not (status and 500 <= status < 600):
                raise
        except (requests.ConnectionError, requests.Timeout):
            pass
        if attempt == MAX_RETRIES:
            raise
        time.sleep(min(BACKOFF_BASE * 2 ** attempt, BACKOFF_CAP))


def tool_summary(messages: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for m in messages:
        if m.get("role") == "assistant":
            for c in m.get("tool_calls") or []:
                counts[c["function"]["name"]] = counts.get(c["function"]["name"], 0) + 1
    return counts


def build_trace(messages: list[dict]) -> dict:
    """Annotate the message trace with tool names.

    Raw tool-result messages only carry tool_call_id; here we map each id back to
    its tool name so every result is self-describing. Also emit a compact
    top-level `tool_calls` list (name + arguments + result) for quick scanning.
    """
    id_to_name = {
        c["id"]: c["function"]["name"]
        for m in messages if m.get("role") == "assistant"
        for c in (m.get("tool_calls") or [])
    }
    result_by_id = {
        m.get("tool_call_id"): m.get("content")
        for m in messages if m.get("role") == "tool"
    }

    annotated = []
    for m in messages:
        if m.get("role") == "tool":
            annotated.append({
                "role": "tool",
                "name": id_to_name.get(m.get("tool_call_id")),
                "tool_call_id": m.get("tool_call_id"),
                "content": m.get("content"),
            })
        else:
            annotated.append(m)

    calls = []
    for m in messages:
        if m.get("role") == "assistant":
            for c in m.get("tool_calls") or []:
                raw = result_by_id.get(c["id"])
                try:
                    result = json.loads(raw) if isinstance(raw, str) else raw
                except (ValueError, TypeError):
                    result = raw
                calls.append({
                    "name": c["function"]["name"],
                    "arguments": json.loads(c["function"]["arguments"] or "{}"),
                    "result": result,
                })

    return {"tool_calls": calls, "messages": annotated}


# Five-way matrix: (config #, mode, system_prompt or None).
# Config 1 is always bare no-rag (no sys, no tools) regardless of --with-system-prompt.
MATRIX_CONFIGS = [
    (1, "no-rag", None),
    (2, "mcp", None),
    (3, "rag", None),
    (4, "mcp", "system"),
    (5, "rag", "system"),
]


def write_output(out_dir: Path, qi: int, mode: str, answer: str, tools: dict | None,
                  system_prompt: str | None, model: str, *, stem: str | None = None) -> None:
    path = out_dir / f"{stem or f'query{qi}_{mode}'}.md"
    tool_line = (
        f"Tool calls: {json.dumps(tools)}" if tools is not None
        else "Tool calls: none (plain model)"
    )
    sp_line = "agent/system_prompt.md" if system_prompt else "none"
    header = (
        f"# Query {qi} — {mode}\n\n"
        f"Model: {model} | Retrieval: {mode} | System prompt: {sp_line}\n"
        f"{tool_line}\n\n"
        f"**Prompt:** {QUERIES[qi - 1]}\n\n---\n\n"
    )
    path.write_text(header + (answer or "[empty answer]"))
    print(f"  saved -> {path.name}")


def run_mode(out_dir: Path, qi: int, mode: str, system_prompt: str | None, model: str,
             *, stem: str | None = None) -> None:
    label = stem or f"query{qi}_{mode}"
    print(f"[query {qi}] {label} mode={mode} model={model} sys={'yes' if system_prompt else 'no'} ...",
          flush=True)
    if mode == "no-rag":
        # Always bare: no system prompt, no tools. See module docstring.
        os.environ.pop("RETRIEVAL_BACKEND", None)
        answer = plain_complete(QUERIES[qi - 1], model, None)
        write_output(out_dir, qi, mode, answer, None, None, model, stem=stem)
        return

    if mode == "rag":
        os.environ.pop("RETRIEVAL_BACKEND", None)  # embeddings path via VECTOR_STORE
    elif mode == "mcp":
        os.environ["RETRIEVAL_BACKEND"] = "mcp"

    answer, messages = run(QUERIES[qi - 1], model=model, system_prompt=system_prompt)
    tools = tool_summary(messages)
    write_output(out_dir, qi, mode, answer, tools, system_prompt, model, stem=stem)
    trace_stem = stem or f"query{qi}_{mode}"
    (out_dir / f"{trace_stem}.trace.json").write_text(
        json.dumps(build_trace(messages), indent=2, default=str)
    )


CELL_RETRIES = 4  # transient connection resets mid-stream are common; retry the whole cell


def run_mode_with_retry(out_dir: Path, qi: int, mode: str, system_prompt: str | None,
                        model: str, *, stem: str | None = None) -> None:
    for attempt in range(CELL_RETRIES + 1):
        try:
            run_mode(out_dir, qi, mode, system_prompt, model, stem=stem)
            return
        except requests.RequestException as e:  # ChunkedEncodingError, ConnectionReset, etc.
            if attempt == CELL_RETRIES:
                raise
            delay = min(BACKOFF_BASE * 2 ** attempt, BACKOFF_CAP) + 1.0
            print(f"  transient {type(e).__name__} on query{qi} {mode}; "
                  f"retry {attempt + 1}/{CELL_RETRIES} in {delay:.0f}s", flush=True)
            time.sleep(delay)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-system-prompt", action="store_true",
                         help="Include agent/system_prompt.md in every call "
                              "(default: no system prompt).")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                         help=f"Output directory (default: {DEFAULT_OUT_DIR}).")
    parser.add_argument("--query", type=int, choices=range(1, len(QUERIES) + 1),
                         metavar="N", help=f"Run only query N (1-{len(QUERIES)}).")
    parser.add_argument("--matrix", action="store_true",
                         help="Run the 5-config matrix (no/sys x no-rag/mcp/rag) "
                              "for the selected --query (or all queries if unset).")
    parser.add_argument("--model", default=MODEL,
                         help=f"OpenRouter model slug (default: {MODEL}).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out_dir
    model = args.model
    system_prompt = SYSTEM_PROMPT if args.with_system_prompt else None
    query_indices = [args.query] if args.query else list(range(1, len(QUERIES) + 1))

    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "_experiment.run.log"

    def log(msg: str) -> None:
        print(msg, flush=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    if args.matrix:
        for qi in query_indices:
            for cfg_num, mode, sp_flag in MATRIX_CONFIGS:
                sp = SYSTEM_PROMPT if sp_flag == "system" else None
                stem = f"query{qi}_cfg{cfg_num}_{mode}"
                try:
                    run_mode_with_retry(out_dir, qi, mode, sp, model, stem=stem)
                except Exception as e:
                    log(f"  FAILED {stem}: {type(e).__name__}: {e}")
                    (out_dir / f"{stem}.ERROR.txt").write_text(f"{type(e).__name__}: {e}")
                time.sleep(2)
        log("done.")
        return

    for qi in query_indices:
        for mode in ("no-rag", "rag", "mcp"):
            try:
                run_mode_with_retry(out_dir, qi, mode, system_prompt, model)
            except Exception as e:
                log(f"  FAILED query{qi} {mode}: {type(e).__name__}: {e}")
                (out_dir / f"query{qi}_{mode}.ERROR.txt").write_text(f"{type(e).__name__}: {e}")
            time.sleep(2)  # be gentle between cells
    log("done.")


if __name__ == "__main__":
    main()
