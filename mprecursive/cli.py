"""CLI entrypoint for MPRecursive.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from colorama import init
except ModuleNotFoundError:
    def init(*_args, **_kwargs):
        return None

from mprecursive.banner import render_banner
from mprecursive.converters.markdown_pdf import MarkdownToPDFConverter
from mprecursive.scanner import scan_files


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="MPRecursive",
        description="Recursively convert markdown files into a single PDF.",
    )
    parser.add_argument("path", help="Root directory to scan")
    parser.add_argument("-o", "--output", default="output.pdf", help="Output PDF file")
    parser.add_argument("--toc", action="store_true", help="Include table of contents")
    parser.add_argument(
        "--sort",
        choices=["name", "modified", "created"],
        default="name",
        help="Sort order for discovered files",
    )
    parser.add_argument("--include-images", action="store_true", help="Reserved option")
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Directory name to ignore (repeatable)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logs")
    parser.add_argument("--engine", default="pandoc", choices=["pandoc"], help="Conversion engine")
    parser.add_argument("--pdf-engine", default="xelatex", help="Pandoc PDF engine")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run MPRecursive CLI."""
    init(autoreset=True)
    print(render_banner())

    parser = build_parser()
    args = parser.parse_args(argv)

    root = Path(args.path)
    output = Path(args.output)

    try:
        files = scan_files(root=root, ignore_dirs=args.ignore, sort_by=args.sort)
    except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not files:
        print("Error: no supported files found in the provided directory.", file=sys.stderr)
        return 1

    converter = MarkdownToPDFConverter(pdf_engine=args.pdf_engine)
    try:
        converter.convert(
            files=files,
            output=output,
            toc=args.toc,
            include_images=args.include_images,
            verbose=args.verbose,
        )
    except (RuntimeError, PermissionError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Successfully generated PDF: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
