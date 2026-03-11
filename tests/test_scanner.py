from pathlib import Path

from mprecursive.scanner import scan_files


def test_scan_files_recursively_and_sort_by_name(tmp_path: Path) -> None:
    (tmp_path / "notes").mkdir()
    (tmp_path / "research").mkdir()
    (tmp_path / "notes" / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "notes" / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "research" / "c.markdown").write_text("c", encoding="utf-8")

    result = scan_files(tmp_path, sort_by="name")

    assert [p.relative_to(tmp_path).as_posix() for p in result] == [
        "notes/a.md",
        "notes/b.md",
        "research/c.markdown",
    ]


def test_scan_files_respects_ignore(tmp_path: Path) -> None:
    (tmp_path / "skip").mkdir()
    (tmp_path / "keep").mkdir()
    (tmp_path / "skip" / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "keep" / "b.md").write_text("b", encoding="utf-8")

    result = scan_files(tmp_path, ignore_dirs=["skip"], sort_by="name")

    assert [p.relative_to(tmp_path).as_posix() for p in result] == ["keep/b.md"]
