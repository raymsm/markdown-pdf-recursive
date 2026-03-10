"""General utility helpers for MPRecursive.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

from __future__ import annotations

import shutil


def ensure_command_exists(command: str) -> None:
    """Raise RuntimeError if command is not available in PATH."""
    if shutil.which(command) is None:
        raise RuntimeError(
            f"Required dependency '{command}' was not found in PATH. "
            "Please install it first."
        )
