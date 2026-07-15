from __future__ import annotations

import json
import urllib.request

import pytest

from harness.agent_models import AGENT_MODEL_OPTIONS, default_model_slug, is_valid_model_slug


@pytest.mark.parametrize("option", AGENT_MODEL_OPTIONS, ids=lambda o: o.slug)
def test_openrouter_slug_exists(option):
    author, slug = option.slug.split("/", 1)
    url = f"https://openrouter.ai/api/v1/model/{author}/{slug}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        payload = json.load(resp)
    assert payload["data"]["id"] == option.slug
    assert option.label in payload["data"]["name"] or payload["data"]["name"].endswith(option.label.split()[-1])


def test_default_model_slug_is_catalog_member():
    assert is_valid_model_slug(default_model_slug())
