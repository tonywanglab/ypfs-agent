"""Record ids for the chat tables, with the same anchored-regex validation the
rest of the harness uses.

A local table rather than an edit to dbio._ID_PATTERNS, so this feature adds no
diff to a shared module. Same contract as dbio.valid_id: routes validate the id
shape before it reaches a query, so a malformed path segment is a 404 rather
than a database round trip.

Ids are `<prefix>_<12 hex>`, matching storage.new_id().
"""

from __future__ import annotations

import re

from ..storage import new_id

PREFIXES = {
    "conversation": "conv",
    "turn": "turn",
    "golden": "gold",
    "revision": "rev",
}

_PATTERNS = {
    kind: re.compile(rf"^{prefix}_[0-9a-f]{{12}}$")
    for kind, prefix in PREFIXES.items()
}


def new(kind: str) -> str:
    """Mint a new id for one of the chat record kinds."""
    try:
        return new_id(PREFIXES[kind])
    except KeyError:
        raise ValueError(f"Unknown chat id kind: {kind!r}") from None


def valid(kind: str, value: str) -> bool:
    pattern = _PATTERNS.get(kind)
    if pattern is None:
        raise ValueError(f"Unknown chat id kind: {kind!r}")
    return bool(value) and bool(pattern.fullmatch(value))


def require(kind: str, value: str) -> str:
    if not valid(kind, value):
        raise ValueError(f"Invalid {kind} id: {value!r}")
    return value
