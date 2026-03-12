from pathlib import Path

import pytest

from mprecursive.cli import build_parser, resolve_input_files


def test_cli_argument_parsing() -> None:
    parser = build_parser()
    args = parser.parse_args([
        "./vault",
        "--output",
        "vault.pdf",
        "--toc",
        "--sort",
        "modified",
        "--ignore",
        ".git",
        "--verbose",
    ])

    assert args.path == "./vault"
    assert args.output == "vault.pdf"
    assert args.toc is True
    assert args.sort == "modified"
    assert args.ignore == [".git"]
    assert args.verbose is True


def test_resolve_input_files_supports_single_markdown_file(tmp_path: Path) -> None:
    file_path = tmp_path / "note.md"
    file_path.write_text("# note", encoding="utf-8")

    files, source_root = resolve_input_files(file_path, ignore_dirs=[], sort_by="name")

    assert files == [file_path]
    assert source_root == tmp_path


def test_resolve_input_files_rejects_unsupported_single_file(tmp_path: Path) -> None:
    file_path = tmp_path / "note.txt"
    file_path.write_text("note", encoding="utf-8")

    with pytest.raises(ValueError):
        resolve_input_files(file_path, ignore_dirs=[], sort_by="name")
