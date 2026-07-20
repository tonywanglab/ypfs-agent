"""Sync client for the local lexical MCP server (the agent-side adapter).

When an MCP retrieval backend is wired in, instantiate one McpClient per
RunContext (agent/context.py) — NOT as a process singleton — so each concurrent
run owns its own server subprocess and session, and call close() when the run
ends. The MCP Python SDK client is async (anyio); we wrap it in a daemon
thread that owns an asyncio loop and keeps one stdio session open for the
client's lifetime, exposing a blocking `call_tool(name, args) -> dict` to the
synchronous agent loop.
"""

import asyncio
import json
import sys
import threading
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent

CALL_TIMEOUT = 120
_MCP_INSTALL_HINT = (
    "Install MCP deps with `.venv/bin/pip install -r requirements.txt` "
    "and run the agent/harness with `.venv/bin/python`."
)


def _import_mcp_sdk():
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"No module named 'mcp'. {_MCP_INSTALL_HINT}"
        ) from e
    return ClientSession, StdioServerParameters, stdio_client


class McpClient:
    """owns a background event loop running one persistent MCP stdio session"""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._session: ClientSession | None = None
        self._shutdown: asyncio.Event | None = None
        self._ready = threading.Event()
        self._error: BaseException | None = None
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._ready.wait()
        if self._error is not None:
            raise self._error

    def _run(self) -> None:
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._serve())
        except BaseException as e:  # surface startup failures to __init__
            if not self._ready.is_set():
                self._error = e
                self._ready.set()

    async def _serve(self) -> None:
        ClientSession, StdioServerParameters, stdio_client = _import_mcp_sdk()
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server"],
            cwd=str(_REPO_ROOT),
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self._session = session
                self._shutdown = asyncio.Event()
                self._ready.set()
                await self._shutdown.wait()  # keep the contexts alive

    def call_tool(self, name: str, arguments: dict) -> dict:
        """Invoke an MCP tool and return its result as a plain dict."""
        if self._session is None:
            return {"error": "MCP session not initialized"}
        fut = asyncio.run_coroutine_threadsafe(
            self._session.call_tool(name, arguments), self._loop
        )
        result = fut.result(timeout=CALL_TIMEOUT)

        # Faithful path: FastMCP serializes the tool's return value as JSON in a
        # text content block. structuredContent carries the same dict on newer
        # SDKs; prefer it when present, else parse the text block.
        sc = getattr(result, "structuredContent", None)
        if isinstance(sc, dict):
            return sc
        for block in result.content:
            text = getattr(block, "text", None)
            if text:
                return json.loads(text)
        if getattr(result, "isError", False):
            return {"error": "MCP tool reported an error"}
        return {"error": "empty MCP tool result"}

    def close(self, timeout: float = 5.0) -> None:
        """Shut down the session, server subprocess, and background thread."""
        if self._shutdown is not None:
            self._loop.call_soon_threadsafe(self._shutdown.set)
        self._thread.join(timeout=timeout)
