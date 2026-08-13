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


def _truncate(text: str, limit: int = 96) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def _pretty_json(value) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, default=str)


def _parse_arguments(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {"_raw": parsed}
    except (TypeError, ValueError):
        return {"_raw": raw}


def _summarize_tool_args(name: str, args: dict) -> str:
    if name == "search_corpus":
        parts = []
        query = args.get("query")
        if query:
            parts.append(f'"{_truncate(query, 72)}"')
        doc_type = args.get("document_type")
        if doc_type:
            parts.append(f"type={doc_type}")
        if args.get("limit") is not None:
            parts.append(f"limit={args['limit']}")
        return " · ".join(parts) if parts else "no query"
    if name == "get_document":
        doc_id = args.get("document_id") or args.get("doc_id")
        return doc_id or "missing document_id"
    if not args:
        return "no arguments"
    return _truncate(_pretty_json(args).replace("\n", " "), 88)


def _summarize_tool_result(name: str, result: dict) -> str:
    if isinstance(result, dict) and "error" in result:
        return f"Error: {_truncate(result['error'], 88)}"
    if name == "search_corpus":
        hits = result.get("results") if isinstance(result, dict) else None
        hits = hits if isinstance(hits, list) else []
        total = result.get("total_found", len(hits)) if isinstance(result, dict) else len(hits)
        doc_ids = [r.get("doc_id") for r in hits if isinstance(r, dict) and r.get("doc_id")]
        if not hits:
            return f"0 hits (total_found={total})"
        preview = ", ".join(doc_ids[:3])
        extra = f" +{len(doc_ids) - 3} more" if len(doc_ids) > 3 else ""
        return f"{len(hits)} hit{'s' if len(hits) != 1 else ''} · {preview}{extra}"
    if name == "get_document":
        if not isinstance(result, dict):
            return "document"
        title = result.get("title")
        doc_id = result.get("doc_id") or result.get("document_id")
        if title and doc_id:
            return f"{doc_id} · {_truncate(title, 64)}"
        return doc_id or (title and _truncate(title, 72)) or "document"
    if isinstance(result, dict):
        keys = ", ".join(sorted(result.keys())[:6])
        return f"keys: {keys}" if keys else "empty result"
    return _truncate(str(result), 88)


def _message_list(trace) -> list[dict]:
    if isinstance(trace, list):
        return trace
    if isinstance(trace, dict):
        messages = trace.get("messages")
        if isinstance(messages, list):
            return messages
    return []


def trace_timeline(trace) -> list[dict]:
    """Turn a persisted agent trace into Cursor-style expandable events.

    Each event has: kind, label, summary, detail (pretty JSON or text).
    Tool call + matching result are paired into one expandable row.
    """
    messages = _message_list(trace)
    id_to_name, id_to_args = _map_tool_call_ids(messages)
    results_by_id: dict[str, dict] = {}
    for message in messages:
        if message.get("role") != "tool":
            continue
        call_id = message.get("tool_call_id")
        if call_id:
            results_by_id[call_id] = {
                "name": message.get("name") or id_to_name.get(call_id, "unknown"),
                "result": _parse_tool_content(message.get("content")),
            }

    events: list[dict] = []
    seen_results: set[str] = set()
    skip_user = True  # Query section already shows the case prompt.

    for message in messages:
        role = message.get("role")
        if role == "user":
            if skip_user:
                skip_user = False
                continue
            content = message.get("content") or ""
            events.append({
                "kind": "user",
                "label": "User",
                "summary": _truncate(content, 140),
                "detail": content,
                "status": "ok",
            })
            continue

        if role == "assistant":
            content = (message.get("content") or "").strip()
            tool_calls = message.get("tool_calls") or []
            if content and not tool_calls:
                events.append({
                    "kind": "assistant",
                    "label": "Assistant",
                    "summary": _truncate(content, 140),
                    "detail": content,
                    "status": "ok",
                })
            elif content and tool_calls:
                events.append({
                    "kind": "assistant",
                    "label": "Assistant",
                    "summary": _truncate(content, 140),
                    "detail": content,
                    "status": "ok",
                })

            for call in tool_calls:
                fn = call.get("function") or {}
                call_id = call.get("id")
                name = fn.get("name") or id_to_name.get(call_id, "unknown")
                args = _parse_arguments(fn.get("arguments"))
                if not args and call_id in id_to_args:
                    args = id_to_args[call_id]
                paired = results_by_id.get(call_id) if call_id else None
                result = paired["result"] if paired else None
                if call_id:
                    seen_results.add(call_id)
                errored = isinstance(result, dict) and "error" in result
                result_summary = (
                    _summarize_tool_result(name, result) if result is not None
                    else "waiting for result"
                )
                events.append({
                    "kind": "tool",
                    "label": name,
                    "summary": _summarize_tool_args(name, args),
                    "result_summary": result_summary,
                    "detail": _pretty_json({
                        "name": name,
                        "call_id": call_id,
                        "arguments": args,
                        "result": result,
                    }),
                    "status": "error" if errored else "ok",
                })
            continue

        if role == "tool":
            call_id = message.get("tool_call_id")
            if call_id and call_id in seen_results:
                continue
            name = message.get("name") or id_to_name.get(call_id, "unknown")
            args = id_to_args.get(call_id, {}) if call_id else {}
            result = _parse_tool_content(message.get("content"))
            errored = isinstance(result, dict) and "error" in result
            events.append({
                "kind": "tool",
                "label": name,
                "summary": _summarize_tool_args(name, args) if args else "tool result",
                "result_summary": _summarize_tool_result(name, result),
                "detail": _pretty_json({
                    "name": name,
                    "call_id": call_id,
                    "arguments": args,
                    "result": result,
                }),
                "status": "error" if errored else "ok",
            })

    return events
