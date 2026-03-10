"""Markdown to PDF converter plugin.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from mprecursive.obsidian import normalize_obsidian_markdown
from mprecursive.utils import ensure_command_exists


class MarkdownToPDFConverter:
    """Pandoc-based markdown-to-PDF conversion pipeline."""

    def __init__(self, pdf_engine: str = "xelatex") -> None:
        self.pdf_engine = pdf_engine

    def convert(
        self,
        files: list[Path],
        output: Path,
        toc: bool = False,
        include_images: bool = False,
        verbose: bool = False,
    ) -> None:
        """Merge and convert markdown files into a single PDF."""
        del include_images  # Reserved for future expansion.

        if not files:
            raise ValueError("No markdown files were found to convert.")

        ensure_command_exists("pandoc")

        with TemporaryDirectory() as temp_dir:
            merged_md = Path(temp_dir) / "merged.md"
            chunks: list[str] = []

            for file in files:
                content = file.read_text(encoding="utf-8", errors="replace")
                normalized = normalize_obsidian_markdown(content)
                title = file.stem.replace("_", " ")
                chunks.append(f"# {title}\n\n{normalized.strip()}\n\n\\newpage\n")

            merged_md.write_text("\n".join(chunks), encoding="utf-8")

            cmd = [
                "pandoc",
                str(merged_md),
                f"--pdf-engine={self.pdf_engine}",
                "-V",
                "geometry:margin=1in",
                "-o",
                str(output),
            ]
            if toc:
                cmd.append("--toc")

            if verbose:
                print("Executing:", " ".join(cmd))

            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
            except FileNotFoundError as exc:
                raise RuntimeError("Pandoc is not installed or not in PATH.") from exc
            except subprocess.CalledProcessError as exc:
                stderr = exc.stderr.strip() if exc.stderr else "Unknown pandoc error"
                raise RuntimeError(f"Pandoc conversion failed: {stderr}") from exc
