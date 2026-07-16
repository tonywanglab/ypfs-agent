"""Thin OpenRouter wrapper shared by judging and version-draft generation.

Mirrors agent/agent.py's retry policy so behavior is consistent, but lives
independently so the crisis-analyst system prompt in agent/system_prompt.md
is never implicitly reused for evaluator-side calls — the evaluator needs
its own, separate persona.

`chat()` is the one seam every higher-level function goes through; tests
monkeypatch it and never hit the network.
"""

from __future__ import annotations

import json
import os
import random
import time

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_TIMEOUT = 120
MAX_RETRIES = 4
BACKOFF_BASE = 1.0
BACKOFF_CAP = 30.0
DEFAULT_MODEL = os.getenv("AGENT_MODEL", "anthropic/claude-sonnet-4.6")
MAX_TOOL_STEPS = 6


class LLMError(Exception):
    """A model call succeeded at the transport level but its content could
    not be used (e.g. malformed JSON after retrying)."""


def _post(messages: list[dict], model: str, tools: list[dict] | None = None,
          json_mode: bool = False) -> dict:
    body = {"model": model, "messages": messages}
    if tools:
        body["tools"] = tools
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json=body,
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]


def chat(messages: list[dict], model: str, tools: list[dict] | None = None,
         json_mode: bool = False) -> dict:
    """One OpenRouter chat completion wrapped in retry/backoff (same policy
    as agent.agent._call): retries connection/timeout errors and HTTP
    429/5xx; other 4xx re-raise immediately."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            return _post(messages, model, tools=tools, json_mode=json_mode)
        except (requests.ConnectionError, requests.Timeout) as e:
            err, retry_after = e, None
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status != 429 and not (status and 500 <= status < 600):
                raise
            err = e
            retry_after = e.response.headers.get("Retry-After") if e.response is not None else None

        if attempt == MAX_RETRIES:
            raise err

        delay = min(BACKOFF_BASE * 2 ** attempt, BACKOFF_CAP) + random.random()
        if retry_after:
            try:
                delay = float(retry_after)
            except ValueError:
                pass
        time.sleep(delay)


def parse_json_object(text: str) -> dict:
    """Parse a JSON object out of model output, tolerating stray prose or
    markdown fences around an otherwise-valid object."""
    text = (text or "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError as e:
            raise LLMError(f"Could not parse a JSON object from model output: {e}\n{text[:500]}")
    raise LLMError(f"Model output did not contain a JSON object.\n{text[:500]}")


def chat_json(system_prompt: str, user_prompt: str, model: str,
              max_attempts: int = 2) -> dict:
    """A single JSON-returning completion, no tools. Retries once on
    malformed JSON with an explicit correction message, then raises."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    last_error: Exception | None = None
    for _ in range(max_attempts):
        msg = chat(messages, model, json_mode=True)
        try:
            return parse_json_object(msg.get("content") or "")
        except LLMError as e:
            last_error = e
            messages.append(msg)
            messages.append({
                "role": "user",
                "content": (f"That was not valid JSON ({e}). Respond with ONLY a valid "
                             "JSON object, no prose, no markdown fences."),
            })
    raise LLMError(f"Model did not return valid JSON after {max_attempts} attempts: {last_error}")


def run_tool_loop(system_prompt: str, user_msg: str, model: str, tools: list[dict],
                   dispatch_fn, max_steps: int = MAX_TOOL_STEPS) -> tuple[str, list[dict]]:
    """A generic, isolated tool loop — same shape as agent.agent.run()'s loop,
    but with its own system prompt/tools/dispatch and fresh history every
    call, so the evaluator never shares memory or persona with the agent it
    is evaluating."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    for _ in range(max_steps):
        msg = chat(messages, model, tools=tools)
        messages.append(msg)
        calls = msg.get("tool_calls")
        if not calls:
            return msg.get("content", ""), messages[1:]
        for c in calls:
            args = json.loads(c["function"]["arguments"] or "{}")
            result = dispatch_fn(c["function"]["name"], args)
            messages.append({
                "role": "tool",
                "tool_call_id": c["id"],
                "content": json.dumps(result, default=str),
            })
    return "[stopped: hit MAX_STEPS]", messages[1:]
