"""Deterministically count tokens for documents grouped by their label.

Each file in text_labeled/ begins with its category on the first line
(e.g. "case_study", "survey"). We count the FULL file contents (label line
included) so results match tokenize_lls.py.

GPT-4o / GPT-5 -> tiktoken o200k_base (local, deterministic)
Claude (latest) -> Anthropic /v1/messages/count_tokens API (deterministic,
                   requires ANTHROPIC_API_KEY + network; no offline tokenizer
                   exists for Claude 3+ models).
"""

import os
import sys
from pathlib import Path

import tiktoken

TEXT_DIR = Path("text_labeled")


def files_for_label(label: str):
    out = []
    for f in sorted(TEXT_DIR.iterdir()):
        if not f.is_file():
            continue
        first = f.read_text(errors="replace").splitlines()
        if first and first[0].strip().lower() == label:
            out.append(f)
    return out


def count_gpt(files, model="gpt-4o"):
    enc = tiktoken.encoding_for_model(model)
    total = 0
    for f in files:
        total += len(enc.encode(f.read_text(errors="replace")))
    return total


def count_claude(files, model):
    """Use Anthropic's official token counting API (deterministic)."""
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    total = 0
    for f in files:
        text = f.read_text(errors="replace")
        resp = client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": text}],
        )
        total += resp.input_tokens
    return total


def main():
    labels = sys.argv[1:] or ["case_study", "survey"]
    claude_models = {
        "Claude Opus (opus-4-1)": "claude-opus-4-1",
        "Claude Sonnet (sonnet-4-5)": "claude-sonnet-4-5",
    }
    have_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

    for label in labels:
        files = files_for_label(label)
        print(f"\n=== {label}: {len(files)} files ===")

        # GPT-4o and GPT-5 share the o200k_base encoding -> identical counts.
        gpt = count_gpt(files, "gpt-4o")
        print(f"GPT-4o / GPT-5 (o200k_base): {gpt:,} tokens")

        if have_key:
            for name, model in claude_models.items():
                try:
                    n = count_claude(files, model)
                    print(f"{name}: {n:,} tokens")
                except Exception as e:  # noqa: BLE001
                    print(f"{name}: ERROR {e}")
        else:
            print("Claude: skipped (set ANTHROPIC_API_KEY to count via API)")


if __name__ == "__main__":
    main()
