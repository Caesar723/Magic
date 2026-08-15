"""TensorBoard-style command line entry point for Synthesis Viewer."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import uvicorn

from .app import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Browse RL synthesis artifacts in a local web UI.")
    parser.add_argument(
        "--logdir",
        required=True,
        help="An experiment directory or a parent directory containing experiments.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=6006, help="TCP port (default: 6006).")
    parser.add_argument("--reload", action="store_true", help="Reload the service when viewer source changes.")
    args = parser.parse_args()

    logdir = Path(args.logdir).expanduser().resolve()
    if not logdir.is_dir():
        parser.error(f"--logdir is not a directory: {logdir}")

    if args.reload:
        os.environ["SYNTHESIS_VIEWER_LOGDIR"] = str(logdir)
        uvicorn.run(
            "game.rlearning.synthesis_viewer.app:app_from_env",
            factory=True,
            host=args.host,
            port=args.port,
            reload=True,
        )
        return

    uvicorn.run(create_app(logdir), host=args.host, port=args.port)


if __name__ == "__main__":
    main()

