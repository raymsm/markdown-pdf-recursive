from mprecursive.obsidian import normalize_obsidian_markdown


def test_normalize_obsidian_markdown() -> None:
    source = "Link: [[my-note]] and image ![[photo.png]] and alias [[doc|Document]]"
    converted = normalize_obsidian_markdown(source)

    assert "my-note" in converted
    assert "![](photo.png)" in converted
    assert "Document" in converted
    assert "[[" not in converted
