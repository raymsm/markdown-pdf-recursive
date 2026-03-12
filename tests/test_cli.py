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


def test_cli_parser_rejects_invalid_pdf_engine() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["./vault", "--pdf-engine", "xelatex;rm -rf /"])


def test_resolve_input_files_returns_absolute_paths(tmp_path: Path) -> None:
    file_path = tmp_path / "note.md"
    file_path.write_text("# note", encoding="utf-8")

    files, source_root = resolve_input_files(file_path, ignore_dirs=[], sort_by="name")

    assert files[0].is_absolute()
    assert source_root.is_absolute()


def test_output_path_is_resolved_absolute(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # minimal main() path through argument parsing without running converter
    from mprecursive import cli as cli_module

    captured = {}

    class _FakeConverter:
        def __init__(self, pdf_engine: str) -> None:
            self.pdf_engine = pdf_engine

        def convert(self, **kwargs):
            captured["output"] = kwargs["output"]

    md_file = tmp_path / "a.md"
    md_file.write_text("# hi", encoding="utf-8")

    monkeypatch.setitem(cli_module.CONVERTER_REGISTRY, "pandoc", _FakeConverter)
    code = cli_module.main([str(md_file), "-o", "out.pdf"])

    assert code == 0
    assert Path(captured["output"]).is_absolute()
