"""Entry point: `python -m mcp_server` builds the index and runs the stdio server."""

from .server import mcp

if __name__ == "__main__":
    # FastMCP defaults to stdio transport — the index builds lazily on first tool call.
    mcp.run()
