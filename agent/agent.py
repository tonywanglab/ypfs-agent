"""
Minimal model-agnostic OpenRouter agent: system prompt + tool registry + loop.

run() is the whole agent: build messages, call the model, run any tool calls,
repeat until the model stops calling tools. It returns (answer, messages) so
evals can assert over both the final text and the full tool trace.
"""

import json
import os
from pathlib import Path
import random
import time

import requests
from dotenv import load_dotenv

from .tools import TOOLS, dispatch

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("AGENT_MODEL", "anthropic/claude-sonnet-4.6")
MAX_STEPS = 10
REQUEST_TIMEOUT = 120

MAX_RETRIES = 4
BACKOFF_BASE = 1.0
BACKOFF_CAP = 30.0

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text().strip()

def _post(messages: list[dict], model: str) -> dict:
    """One OpenRouter chat completion. Returns the assistant message dict."""
    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json={"model": model, "messages": messages, "tools": TOOLS},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]


def _call(messages: list[dict], model: str) -> dict:
    """_post wrapped in retry/backoff. Retries transient failures only:
    connection/timeout errors and HTTP 429/5xx. Other 4xx re-raise immediately."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            return _post(messages, model)
        except (requests.ConnectionError, requests.Timeout) as e:
            err, retry_after = e, None
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status != 429 and not (status and 500 <= status < 600):
                raise  # non-retryable (4xx other than 429)
            err = e
            retry_after = e.response.headers.get("Retry-After") if e.response is not None else None

        if attempt == MAX_RETRIES:
            raise err  # out of retries

        delay = min(BACKOFF_BASE * 2 ** attempt, BACKOFF_CAP) + random.random()
        if retry_after:  # honor server's Retry-After on 429 when present
            try:
                delay = float(retry_after)
            except ValueError:
                pass
        time.sleep(delay)


def run(user_msg: str, history: list[dict] | None = None, model: str = DEFAULT_MODEL,
        system_prompt: str | None = SYSTEM_PROMPT):
    """Run the agent loop until the model stops calling tools.

    history excludes the system prompt, so the returned messages round-trip
    cleanly back in as the next call's history. Pass system_prompt=None to
    omit the system prompt entirely.

    Returns (answer: str, messages: list[dict]) — messages is the full trace
    (user/assistant/tool turns) for eval inspection.
    """
    messages = [*([ {"role": "system", "content": system_prompt}] if system_prompt else []),
                *(history or []),
                {"role": "user", "content": user_msg}]

    for _ in range(MAX_STEPS):
        msg = _call(messages, model)
        messages.append(msg)
        calls = msg.get("tool_calls")
        if not calls:
            return msg.get("content", ""), messages[1:]
        for c in calls:
            args = json.loads(c["function"]["arguments"] or "{}")
            result = dispatch(c["function"]["name"], args)
            messages.append({
                "role": "tool",
                "tool_call_id": c["id"],
                "content": json.dumps(result, default=str),
            })

    return "[stopped: hit MAX_STEPS]", messages[1:]


SMOKE_CASES = [
    ("retrieval",  "What programs did the Fed use during the 2008 financial crisis?"),
    ("comparison", "Compare deposit guarantee schemes across countries."),
    ("synthesis",  "What do surveys say about the effectiveness of capital injections?"),
]


def _print_trace(messages: list[dict]) -> None:
    for m in messages:
        if m.get("role") == "assistant":
            for c in m.get("tool_calls", []):
                fn = c["function"]
                args = json.loads(fn.get("arguments") or "{}")
                print(f"  [tool call] {fn['name']}({json.dumps(args, separators=(',', ':'))})")
        elif m.get("role") == "tool":
            try:
                data = json.loads(m.get("content", "{}"))
                results = data.get("results", [])
                if results:
                    titles = [r.get("title", r.get("doc_id", "?"))[:60] for r in results[:3]]
                    suffix = f" (+{len(results)-3} more)" if len(results) > 3 else ""
                    print(f"  [tool result] total_found={data.get('total_found')} → {titles}{suffix}")
                elif "error" in data:
                    print(f"  [tool error] {data['error']}")
                else:
                    print(f"  [tool result] {list(data.keys())}")
            except Exception:
                print(f"  [tool result] {m.get('content', '')[:120]}")


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="YPFS agent REPL / test runner.")
    parser.add_argument("-q", "--query", help="Run a single query and exit.")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"OpenRouter model slug (default: {DEFAULT_MODEL}).")
    parser.add_argument("--verbose", action="store_true",
                        help="Print tool-call trace after each turn.")
    parser.add_argument("--no-system-prompt", action="store_true",
                        help="Omit the system prompt entirely.")
    parser.add_argument("--save", metavar="FILE",
                        help="Save the answer to this file path.")
    parser.add_argument("--smoke", action="store_true",
                        help="Run built-in smoke cases and exit 0/1.")
    args = parser.parse_args()

    model = args.model
    system_prompt = None if args.no_system_prompt else SYSTEM_PROMPT

    if args.smoke:
        passed = 0
        for name, q in SMOKE_CASES:
            print(f"=== {name} ===\nyou> {q}")
            answer, messages = run(q, model=model, system_prompt=system_prompt)
            if args.verbose:
                _print_trace(messages)
            tool_turns = sum(1 for m in messages if m.get("role") == "tool")
            ok = bool(answer and tool_turns > 0)
            print(f"agent> {answer}")
            print(f"[{'PASS' if ok else 'FAIL'}] tools called: {tool_turns}\n")
            passed += ok
        print(f"{passed}/{len(SMOKE_CASES)} passed")
        sys.exit(0 if passed == len(SMOKE_CASES) else 1)

    if args.query:
        answer, messages = run(args.query, model=model, system_prompt=system_prompt)
        if args.verbose:
            _print_trace(messages)
        print(f"agent> {answer}")
        if args.save:
            Path(args.save).parent.mkdir(parents=True, exist_ok=True)
            Path(args.save).write_text(answer)
            print(f"saved → {args.save}")
        return

    print(f"agent ready (model: {model}). Ctrl-D to exit.\n")
    history: list[dict] = []
    while True:
        try:
            q = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            continue
        answer, history = run(q, history=history, model=model, system_prompt=system_prompt)
        if args.verbose:
            _print_trace(history)
        print(f"\nagent> {answer}\n")
