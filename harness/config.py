"""Fixed model configuration for the evaluation harness."""

from __future__ import annotations

import os


DEFAULT_AGENT_MODEL = "anthropic/claude-fable-5"
DEFAULT_EDITOR_MODEL = "openai/gpt-5.6-terra"


def agent_model() -> str:
    return os.environ.get("HARNESS_AGENT_MODEL", DEFAULT_AGENT_MODEL)


def editor_model() -> str:
    return os.environ.get("HARNESS_EDITOR_MODEL", DEFAULT_EDITOR_MODEL)
