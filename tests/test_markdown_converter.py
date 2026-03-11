from pathlib import Path

from mprecursive.converters.markdown_pdf import _resolve_relative_images, _strip_front_matter


def test_strip_front_matter_removes_leading_yaml_block() -> None:
    source = """---
title: Test
bad yaml line without colon
---
# Heading
Body
"""
    result = _strip_front_matter(source)
    assert result.startswith("# Heading")
    assert "title:" not in result


def test_strip_front_matter_no_block_unchanged() -> None:
    source = "# Heading\n---\nnot front matter\n"
    assert _strip_front_matter(source) == source


def test_resolve_relative_images_converts_local_paths(tmp_path: Path) -> None:
    text = "Image ![](pics/a.png) remote ![](https://example.com/a.png)"
    result = _resolve_relative_images(text, tmp_path)
    assert f"![]({(tmp_path / 'pics/a.png').resolve().as_posix()})" in result
    assert "https://example.com/a.png" in result
