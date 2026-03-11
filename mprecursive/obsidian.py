"""Obsidian-flavored markdown conversion helpers.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

from __future__ import annotations

import re

IMAGE_PATTERN = re.compile(r"!\[\[([^\]]+)\]\]")
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def normalize_obsidian_markdown(text: str) -> str:
    """Convert Obsidian wiki/image links to standard markdown.

    - ``![[image.png]]`` -> ``![](image.png)``
    - ``[[note]]`` -> ``note``
    - ``[[path|Label]]`` -> ``Label``
    """

    text = IMAGE_PATTERN.sub(r"![](\1)", text)

    def _wikilink_replace(match: re.Match[str]) -> str:
        target = match.group(1)
        alias = match.group(2)
        return alias if alias else target

    return WIKILINK_PATTERN.sub(_wikilink_replace, text)
