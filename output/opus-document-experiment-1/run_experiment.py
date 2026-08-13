"""Opus document experiment: 3 scenario queries x 3 retrieval modes.

For each query, opus-4.8 answers with NO system prompt under three conditions:
  - no-rag : plain model, no tools at all (pure parametric knowledge)
  - rag    : embeddings RAG via the default vector store (Pinecone)
  - mcp    : embedding-free lexical retrieval via the local BM25 MCP server

Run from the repo root:  .venv/bin/python output/opus-document-experiment/run_experiment.py

Outputs (this folder): query{n}_{mode}.md  (header + answer)
                       query{n}_{mode}.trace.json  (tool trace, RAG/MCP only)
"""

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
    API_URL, REQUEST_TIMEOUT, MAX_RETRIES, BACKOFF_BASE, BACKOFF_CAP, run,
)

MODEL = "anthropic/claude-opus-4.8"
OUT_DIR = Path(__file__).resolve().parent

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


def plain_complete(user_msg: str, model: str) -> str:
    """One chat completion with NO tools and NO system prompt (the no-rag baseline).

    Mirrors agent.agent._call's retry policy but omits the `tools` key entirely
    (an empty tools array is rejected by some providers).
    """
    body = {"model": model, "messages": [{"role": "user", "content": user_msg}]}
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


def write_output(qi: int, mode: str, answer: str, tools: dict | None) -> None:
    path = OUT_DIR / f"query{qi}_{mode}.md"
    tool_line = (
        f"Tool calls: {json.dumps(tools)}" if tools is not None
        else "Tool calls: none (plain model)"
    )
    header = (
        f"# Query {qi} — {mode}\n\n"
        f"Model: {MODEL} | Retrieval: {mode} | System prompt: none\n"
        f"{tool_line}\n\n"
        f"**Prompt:** {QUERIES[qi - 1]}\n\n---\n\n"
    )
    path.write_text(header + (answer or "[empty answer]"))
    print(f"  saved -> {path.name}")


def run_mode(qi: int, mode: str) -> None:
    print(f"[query {qi}] mode={mode} ...", flush=True)
    if mode == "no-rag":
        os.environ.pop("RETRIEVAL_BACKEND", None)
        answer = plain_complete(QUERIES[qi - 1], MODEL)
        write_output(qi, mode, answer, None)
        return

    if mode == "rag":
        os.environ.pop("RETRIEVAL_BACKEND", None)  # default VECTOR_STORE=pinecone
    elif mode == "mcp":
        os.environ["RETRIEVAL_BACKEND"] = "mcp"

    answer, messages = run(QUERIES[qi - 1], model=MODEL, system_prompt=None)
    tools = tool_summary(messages)
    write_output(qi, mode, answer, tools)
    (OUT_DIR / f"query{qi}_{mode}.trace.json").write_text(json.dumps(messages, indent=2, default=str))


CELL_RETRIES = 4  # transient connection resets mid-stream are common; retry the whole cell


def run_mode_with_retry(qi: int, mode: str) -> None:
    for attempt in range(CELL_RETRIES + 1):
        try:
            run_mode(qi, mode)
            return
        except requests.RequestException as e:  # ChunkedEncodingError, ConnectionReset, etc.
            if attempt == CELL_RETRIES:
                raise
            delay = min(BACKOFF_BASE * 2 ** attempt, BACKOFF_CAP) + 1.0
            print(f"  transient {type(e).__name__} on query{qi} {mode}; "
                  f"retry {attempt + 1}/{CELL_RETRIES} in {delay:.0f}s", flush=True)
            time.sleep(delay)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for qi in range(1, len(QUERIES) + 1):
        for mode in ("no-rag", "rag", "mcp"):
            try:
                run_mode_with_retry(qi, mode)
            except Exception as e:
                print(f"  FAILED query{qi} {mode}: {type(e).__name__}: {e}", flush=True)
                (OUT_DIR / f"query{qi}_{mode}.ERROR.txt").write_text(f"{type(e).__name__}: {e}")
            time.sleep(2)  # be gentle between cells
    print("done.")


if __name__ == "__main__":
    main()
