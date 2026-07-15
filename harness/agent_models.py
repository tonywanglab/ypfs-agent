"""Curated OpenRouter agent models for the chat launcher.

Slugs verified against GET https://openrouter.ai/api/v1/model/{author}/{slug}
on 2026-07-15.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.agent import DEFAULT_MODEL


@dataclass(frozen=True)
class AgentModelOption:
    label: str
    slug: str


# Latest frontier chat models with tool-calling support.
AGENT_MODEL_OPTIONS: tuple[AgentModelOption, ...] = (
    AgentModelOption("Claude Sonnet 4.6", "anthropic/claude-sonnet-4.6"),
    AgentModelOption("Claude Sonnet 5", "anthropic/claude-sonnet-5"),
    AgentModelOption("Claude Opus 4.8", "anthropic/claude-opus-4.8"),
    AgentModelOption("GPT-5.4", "openai/gpt-5.4"),
    AgentModelOption("GPT-5.5", "openai/gpt-5.5"),
    AgentModelOption("GPT-5.2", "openai/gpt-5.2"),
    AgentModelOption("Gemini 2.5 Pro", "google/gemini-2.5-pro"),
    AgentModelOption("Gemini 3.1 Pro Preview", "google/gemini-3.1-pro-preview"),
    AgentModelOption("Gemini 3.5 Flash", "google/gemini-3.5-flash"),
)

_SLUGS = {m.slug for m in AGENT_MODEL_OPTIONS}


def is_valid_model_slug(slug: str) -> bool:
    return slug in _SLUGS


def default_model_slug() -> str:
    preferred = __import__("os").environ.get("AGENT_MODEL", DEFAULT_MODEL)
    if preferred in _SLUGS:
        return preferred
    if DEFAULT_MODEL in _SLUGS:
        return DEFAULT_MODEL
    return AGENT_MODEL_OPTIONS[0].slug
