"""Curated OpenRouter agent models for the chat launcher.

Slugs verified against GET https://openrouter.ai/api/v1/model/{author}/{slug}
on 2026-07-15.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentModelOption:
    label: str
    slug: str


# Latest frontier chat models with tool-calling support.
AGENT_MODEL_OPTIONS: tuple[AgentModelOption, ...] = (
    # Anthropic
    AgentModelOption("Claude Sonnet 4.6", "anthropic/claude-sonnet-4.6"),
    AgentModelOption("Claude Sonnet 5", "anthropic/claude-sonnet-5"),
    AgentModelOption("Claude Opus 4.8", "anthropic/claude-opus-4.8"),
    AgentModelOption("Claude Fable 5", "anthropic/claude-fable-5"),
    # OpenAI GPT-5 family
    AgentModelOption("GPT-5", "openai/gpt-5"),
    AgentModelOption("GPT-5 Pro", "openai/gpt-5-pro"),
    AgentModelOption("GPT-5 Chat", "openai/gpt-5-chat"),
    AgentModelOption("GPT-5 Mini", "openai/gpt-5-mini"),
    AgentModelOption("GPT-5 Nano", "openai/gpt-5-nano"),
    AgentModelOption("GPT-5 Codex", "openai/gpt-5-codex"),
    AgentModelOption("GPT-5.1", "openai/gpt-5.1"),
    AgentModelOption("GPT-5.1 Chat", "openai/gpt-5.1-chat"),
    AgentModelOption("GPT-5.1 Codex", "openai/gpt-5.1-codex"),
    AgentModelOption("GPT-5.1 Codex Max", "openai/gpt-5.1-codex-max"),
    AgentModelOption("GPT-5.1 Codex Mini", "openai/gpt-5.1-codex-mini"),
    AgentModelOption("GPT-5.2", "openai/gpt-5.2"),
    AgentModelOption("GPT-5.2 Pro", "openai/gpt-5.2-pro"),
    AgentModelOption("GPT-5.2 Chat", "openai/gpt-5.2-chat"),
    AgentModelOption("GPT-5.2 Codex", "openai/gpt-5.2-codex"),
    AgentModelOption("GPT-5.3 Chat", "openai/gpt-5.3-chat"),
    AgentModelOption("GPT-5.3 Codex", "openai/gpt-5.3-codex"),
    AgentModelOption("GPT-5.4", "openai/gpt-5.4"),
    AgentModelOption("GPT-5.4 Pro", "openai/gpt-5.4-pro"),
    AgentModelOption("GPT-5.4 Mini", "openai/gpt-5.4-mini"),
    AgentModelOption("GPT-5.4 Nano", "openai/gpt-5.4-nano"),
    AgentModelOption("GPT-5.5", "openai/gpt-5.5"),
    AgentModelOption("GPT-5.5 Pro", "openai/gpt-5.5-pro"),
    AgentModelOption("GPT-5.6 Sol", "openai/gpt-5.6-sol"),
    AgentModelOption("GPT-5.6 Sol Pro", "openai/gpt-5.6-sol-pro"),
    AgentModelOption("GPT-5.6 Luna", "openai/gpt-5.6-luna"),
    AgentModelOption("GPT-5.6 Luna Pro", "openai/gpt-5.6-luna-pro"),
    AgentModelOption("GPT-5.6 Terra", "openai/gpt-5.6-terra"),
    AgentModelOption("GPT-5.6 Terra Pro", "openai/gpt-5.6-terra-pro"),
    # Google
    AgentModelOption("Gemini 2.5 Pro", "google/gemini-2.5-pro"),
    AgentModelOption("Gemini 3.1 Pro Preview", "google/gemini-3.1-pro-preview"),
    AgentModelOption("Gemini 3.5 Flash", "google/gemini-3.5-flash"),
)

DEFAULT_CHAT_MODEL = "anthropic/claude-fable-5"

_SLUGS = {m.slug for m in AGENT_MODEL_OPTIONS}


def is_valid_model_slug(slug: str) -> bool:
    return slug in _SLUGS


def default_model_slug() -> str:
    preferred = __import__("os").environ.get("AGENT_MODEL")
    if preferred and preferred in _SLUGS:
        return preferred
    return DEFAULT_CHAT_MODEL
