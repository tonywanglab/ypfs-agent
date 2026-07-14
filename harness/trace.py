"""Normalize agent.run() message traces into a structure the deterministic
checks and the judge can consume without re-parsing tool JSON everywhere.

Works on the message shape returned by agent.agent.run(): a list of
user/assistant/tool dicts (system prompt already stripped), with tool
results JSON-stringified in each tool message's "content" and the calling
tool name recoverable via tool_call_id -> the assistant message that issued
the call. Also tolerates an already-annotated tool message that carries its
own "name" field, so saved traces round-trip through build_trace() cleanly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

MAX_STEPS_SENTINEL = "[stopped: hit MAX_STEPS]"


@dataclass
class ToolCall:
    call_id: str | None
    name: str
    arguments: dict
    result: dict

    def to_dict(self) -> dict:
        return {"call_id": self.call_id, "name": self.name, "arguments": self.arguments,
                "result": self.result}


@dataclass
class NormalizedTrace:
    tool_calls: list[ToolCall] = field(default_factory=list)
    retrieved_doc_ids: set[str] = field(default_factory=set)
    fetched_doc_ids: set[str] = field(default_factory=set)
    tool_errors: list[dict] = field(default_factory=list)
    tool_counts: dict = field(default_factory=dict)
    hit_max_steps: bool = False

    def to_dict(self) -> dict:
        return {
            "tool_calls": [c.to_dict() for c in self.tool_calls],
            "retrieved_doc_ids": sorted(self.retrieved_doc_ids),
            "fetched_doc_ids": sorted(self.fetched_doc_ids),
            "tool_errors": self.tool_errors,
            "tool_counts": self.tool_counts,
            "hit_max_steps": self.hit_max_steps,
        }


def _parse_tool_content(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {"_raw": parsed}
    except (TypeError, ValueError):
        return {"_raw": raw}


def _map_tool_call_ids(messages: list[dict]) -> tuple[dict, dict]:
    """tool_call_id -> (name, arguments), read off assistant tool_calls."""
    id_to_name: dict[str, str] = {}
    id_to_args: dict[str, dict] = {}
    for m in messages:
        if m.get("role") != "assistant":
            continue
        for c in m.get("tool_calls") or []:
            fn = c.get("function", {})
            call_id = c.get("id")
            if not call_id:
                continue
            id_to_name[call_id] = fn.get("name", "unknown")
            try:
                id_to_args[call_id] = json.loads(fn.get("arguments") or "{}")
            except (TypeError, ValueError):
                id_to_args[call_id] = {}
    return id_to_name, id_to_args


def normalize_messages(messages: list[dict], answer: str | None = None) -> NormalizedTrace:
    """Build a NormalizedTrace from agent.run()'s returned `messages` list."""
    trace = NormalizedTrace()
    id_to_name, id_to_args = _map_tool_call_ids(messages)

    for m in messages:
        if m.get("role") != "tool":
            continue
        call_id = m.get("tool_call_id")
        name = m.get("name") or id_to_name.get(call_id, "unknown")
        args = id_to_args.get(call_id, {})
        result = _parse_tool_content(m.get("content"))

        trace.tool_calls.append(ToolCall(call_id=call_id, name=name, arguments=args, result=result))
        trace.tool_counts[name] = trace.tool_counts.get(name, 0) + 1

        if isinstance(result, dict) and "error" in result:
            trace.tool_errors.append({"tool_name": name, "arguments": args, "error": result["error"]})
            continue

        if name == "search_corpus":
            for r in (result.get("results") or []):
                doc_id = r.get("doc_id")
                if doc_id:
                    trace.retrieved_doc_ids.add(doc_id)
        elif name == "get_document":
            doc_id = result.get("doc_id")
            if doc_id:
                trace.fetched_doc_ids.add(doc_id)

    if answer is not None and answer.strip() == MAX_STEPS_SENTINEL:
        trace.hit_max_steps = True

    return trace


def tool_summary(messages: list[dict]) -> dict:
    """{"search_corpus": N, "get_document": M} style counts."""
    return normalize_messages(messages).tool_counts


def build_trace(messages: list[dict], answer: str | None = None) -> dict:
    """Serializable trace shape for persistence: annotated raw messages (tool
    turns get their name attached) plus the normalized summary used by
    checks/judging."""
    normalized = normalize_messages(messages, answer=answer)
    id_to_name, _ = _map_tool_call_ids(messages)

    annotated = []
    for m in messages:
        if m.get("role") == "tool":
            annotated.append({
                "role": "tool",
                "name": m.get("name") or id_to_name.get(m.get("tool_call_id")),
                "tool_call_id": m.get("tool_call_id"),
                "content": m.get("content"),
            })
        else:
            annotated.append(m)

    return {"messages": annotated, "normalized": normalized.to_dict()}
