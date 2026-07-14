"""CLI entry point: python -m harness"""

from __future__ import annotations

import argparse

from . import seed
from .web import main as web_main


def _cmd_seed(_args: argparse.Namespace) -> None:
    seed.seed_all()
    print(f"Seeded harness data under {seed.EVALS_DIR}")


def _cmd_web(args: argparse.Namespace) -> None:
    web_main(host=args.host, port=args.port, debug=args.debug)


def main() -> None:
    parser = argparse.ArgumentParser(description="YPFS evaluation harness")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("seed", help="Seed cases, rubric v1, and prompt v1")

    web_p = sub.add_parser("web", help="Start the local supervisor UI")
    web_p.add_argument("--host", default="127.0.0.1")
    web_p.add_argument("--port", type=int, default=5050)
    web_p.add_argument("--debug", action="store_true")

    args = parser.parse_args()
    if args.command == "seed":
        _cmd_seed(args)
    elif args.command == "web":
        _cmd_web(args)
    else:
        # Default: start the supervisor UI (plan: python -m harness)
        web_main()


if __name__ == "__main__":
    main()
