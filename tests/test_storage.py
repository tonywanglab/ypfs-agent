from __future__ import annotations

import pytest

from harness.storage import (
    atomic_write_json,
    atomic_write_text,
    append_jsonl,
    read_json,
    read_json_default,
    read_jsonl,
    rewrite_jsonl,
    safe_path,
)


def test_atomic_write_and_read_json(tmp_path):
    path = tmp_path / "sub" / "thing.json"
    atomic_write_json(path, {"a": 1, "b": [1, 2, 3]})
    assert read_json(path) == {"a": 1, "b": [1, 2, 3]}


def test_atomic_write_leaves_no_tmp_file_behind(tmp_path):
    path = tmp_path / "thing.json"
    atomic_write_json(path, {"a": 1})
    leftovers = list(tmp_path.glob(".*.tmp"))
    assert leftovers == []


def test_read_json_default_missing(tmp_path):
    assert read_json_default(tmp_path / "missing.json", "fallback") == "fallback"


def test_jsonl_append_and_read(tmp_path):
    path = tmp_path / "rows.jsonl"
    append_jsonl(path, {"id": 1})
    append_jsonl(path, {"id": 2})
    assert read_jsonl(path) == [{"id": 1}, {"id": 2}]


def test_read_jsonl_missing_file_returns_empty(tmp_path):
    assert read_jsonl(tmp_path / "missing.jsonl") == []


def test_rewrite_jsonl_replaces_contents(tmp_path):
    path = tmp_path / "rows.jsonl"
    append_jsonl(path, {"id": 1})
    append_jsonl(path, {"id": 2})
    rewrite_jsonl(path, [{"id": 1, "updated": True}])
    assert read_jsonl(path) == [{"id": 1, "updated": True}]


def test_safe_path_rejects_traversal(tmp_path):
    with pytest.raises(ValueError):
        safe_path("..", "escaped.json", base=tmp_path)


def test_safe_path_allows_nested(tmp_path):
    p = safe_path("nested", "file.json", base=tmp_path)
    assert p == (tmp_path / "nested" / "file.json").resolve()
