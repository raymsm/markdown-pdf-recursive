"""Filesystem scanning logic for MPRecursive.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {".md", ".markdown"}


def scan_files(
    root: Path,
    extensions: Iterable[str] = SUPPORTED_EXTENSIONS,
    ignore_dirs: list[str] | None = None,
    sort_by: str = "name",
) -> list[Path]:
    """Recursively collect supported files from *root*.

    Args:
        root: Root directory to scan.
        extensions: Allowed suffixes.
        ignore_dirs: Directory names to skip.
        sort_by: One of ``name``, ``modified``, ``created``.
    """
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")

    ignore = {item.strip() for item in (ignore_dirs or []) if item.strip()}
    exts = {ext.lower() for ext in extensions}

    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in ignore for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in exts:
            files.append(path)

    if sort_by == "name":
        files.sort(key=lambda p: str(p.relative_to(root)).lower())
    elif sort_by == "modified":
        files.sort(key=lambda p: p.stat().st_mtime)
    elif sort_by == "created":
        files.sort(key=lambda p: p.stat().st_ctime)
    else:
        raise ValueError(f"Unsupported sort mode: {sort_by}")

    return files
