"""Markdown to PDF converter plugin.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from mprecursive.obsidian import normalize_obsidian_markdown
from mprecursive.utils import ensure_command_exists

FRONT_MATTER_START = "---"
FRONT_MATTER_END = {"---", "..."}
IMAGE_LINK_PATTERN = re.compile(r"!\[(.*?)\]\(([^)\s]+)(?:\s+\".*?\")?\)")


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
        source_root: Path | None = None,
    ) -> None:
        """Merge and convert markdown files into a single PDF."""
        del include_images  # Reserved for future expansion.

        if not files:
            raise ValueError("No markdown files were found to convert.")

        ensure_command_exists("pandoc")

        resource_root = source_root.resolve() if source_root else files[0].resolve().parent

        with TemporaryDirectory() as temp_dir:
            merged_md = Path(temp_dir) / "merged.md"
            chunks: list[str] = []

            for file in files:
                content = file.read_text(encoding="utf-8", errors="replace")
                normalized = normalize_obsidian_markdown(content)
                without_front_matter = _strip_front_matter(normalized)
                resolved_images = _resolve_relative_images(without_front_matter, file.parent)
                title = file.stem.replace("_", " ")
                chunks.append(f"# {title}\n\n{resolved_images.strip()}\n\n\\newpage\n")

            merged_md.write_text("\n".join(chunks), encoding="utf-8")

            cmd = [
                "pandoc",
                str(merged_md),
                "--from=markdown-yaml_metadata_block",
                f"--pdf-engine={self.pdf_engine}",
                "--resource-path",
                str(resource_root),
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
                if "not found" in stderr.lower() and "pdf-engine" in stderr.lower():
                    raise RuntimeError(
                        "Pandoc PDF engine was not found. Install the selected engine "
                        f"('{self.pdf_engine}') or pass --pdf-engine with an available option."
                    ) from exc
                raise RuntimeError(f"Pandoc conversion failed: {stderr}") from exc


def _strip_front_matter(text: str) -> str:
    """Strip a leading YAML front-matter block from markdown text."""
    lines = text.splitlines()
    if not lines:
        return text

    first_nonempty_idx = next((i for i, line in enumerate(lines) if line.strip()), None)
    if first_nonempty_idx is None or lines[first_nonempty_idx].strip() != FRONT_MATTER_START:
        return text

    for idx in range(first_nonempty_idx + 1, len(lines)):
        if lines[idx].strip() in FRONT_MATTER_END:
            return "\n".join(lines[idx + 1 :]).lstrip("\n")

    return text


def _resolve_relative_images(text: str, base_dir: Path) -> str:
    """Resolve markdown image links against *base_dir* to avoid missing resources."""

    def _replace(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        target = match.group(2)
        if target.startswith(("http://", "https://", "file://", "/", "#")):
            return match.group(0)

        absolute_target = (base_dir / target).resolve()
        return f"![{alt_text}]({absolute_target.as_posix()})"

    return IMAGE_LINK_PATTERN.sub(_replace, text)
