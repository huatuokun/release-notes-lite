from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .formatting import format_markdown, format_text
from .generator import generate_release_notes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="release-notes", description="Generate concise release notes from git commits.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate notes for a git range.")
    generate_parser.add_argument("--range", dest="revision_range", required=True, help="Git revision range, for example v0.1.0..HEAD")
    generate_parser.add_argument("--root", default=".", help="Repository root path.")
    generate_parser.add_argument("--format", choices=("text", "markdown"), default="text", help="Output format.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        try:
            commits = generate_release_notes(Path(args.root), args.revision_range)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        output = format_markdown(commits) if args.format == "markdown" else format_text(commits)
        print(output, end="")
        return 0

    parser.error("Unknown command")
    return 2
