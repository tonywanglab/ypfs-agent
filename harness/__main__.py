"""CLI entry point: python -m harness"""

from __future__ import annotations

import argparse
import os
import sys
import threading

from . import seed
from .web import main as web_main


def _require_database_url() -> None:
    if not os.getenv("DATABASE_URL"):
        sys.exit(
            "DATABASE_URL not set. Add it to .env, e.g.\n"
            "  DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require\n"
            "The harness stores cases, versions, runs, reviews, and tasks in Postgres."
        )


def _require_mcp_deps() -> None:
    """Default retrieval is MCP (BM25 server); fail fast with install instructions."""
    if os.getenv("RETRIEVAL_BACKEND", "mcp") != "mcp":
        return
    try:
        import mcp  # noqa: F401
        import rank_bm25  # noqa: F401
    except ModuleNotFoundError as e:
        sys.exit(
            f"{e}\n\n"
            "The default RETRIEVAL_BACKEND=mcp needs the MCP SDK and rank-bm25.\n"
            "  .venv/bin/pip install -r requirements.txt\n"
            "Then start the harness with the project venv:\n"
            "  .venv/bin/python -m harness web --with-worker"
        )


def _cmd_seed(_args: argparse.Namespace) -> None:
    seed.seed_all()
    print(f"Seeded {len(seed.load_cases())} cases, rubric_v1, prompt_v1 into Postgres")


def _cmd_web(args: argparse.Namespace) -> None:
    stop_event = None
    if args.with_worker:
        from . import worker

        stop_event = threading.Event()
        worker.start_workers(args.worker_concurrency, stop_event, daemon=True)
    web_main(host=args.host, port=args.port, debug=args.debug)
    if stop_event is not None:
        stop_event.set()


def _cmd_worker(args: argparse.Namespace) -> None:
    from . import worker

    worker.main(concurrency=args.concurrency)


def main() -> None:
    parser = argparse.ArgumentParser(description="YPFS evaluation harness")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("seed", help="Seed cases, rubric v1, and prompt v1")

    web_p = sub.add_parser("web", help="Start the local supervisor UI")
    web_p.add_argument("--host", default="127.0.0.1")
    web_p.add_argument("--port", type=int, default=5050)
    web_p.add_argument("--debug", action="store_true")
    web_p.add_argument("--with-worker", action="store_true",
                       help="Also run the task queue worker in-process (dev convenience)")
    web_p.add_argument("--worker-concurrency", type=int,
                       default=int(os.getenv("HARNESS_WORKER_CONCURRENCY", "3")))

    worker_p = sub.add_parser("worker", help="Run the task queue worker pool")
    worker_p.add_argument("--concurrency", type=int,
                          default=int(os.getenv("HARNESS_WORKER_CONCURRENCY", "3")))

    args = parser.parse_args()
    _require_database_url()
    _require_mcp_deps()
    if args.command == "seed":
        _cmd_seed(args)
    elif args.command == "web":
        _cmd_web(args)
    elif args.command == "worker":
        _cmd_worker(args)
    else:
        # Default: start the supervisor UI (plan: python -m harness)
        web_main()


if __name__ == "__main__":
    main()
