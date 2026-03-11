# MPRecursive

A professional, modular CLI for recursive document conversion workflows, starting with **Markdown → PDF**.

**Developed by raymsm**  
**GitHub: https://github.com/raymsm**

---

## Overview

`MPRecursive` scans a directory tree, detects supported files, and converts them into a single output document. The first production pipeline is markdown aggregation and PDF generation powered by Pandoc.

## Features

- Recursive directory scanning for markdown files
- Deterministic sorting (`name`, `modified`, `created`)
- Merge all discovered markdown files into one PDF with per-file sections
- Automatic Obsidian syntax normalization:
  - `[[wikilink]]` → `wikilink`
  - `![[image.png]]` → `![](image.png)`
- Strips leading YAML front matter per file before merge to avoid malformed metadata crashes
- Resolves local image paths against each source note directory for more reliable Pandoc resource loading
- Table of contents support via Pandoc
- Modular converter architecture for future pipelines
- Colorful startup banner with developer attribution

## Installation

### From PyPI

```bash
pip install markdown-pdf-recursive
```

### Manual install (editable)

```bash
git clone https://github.com/raymsm/markdown-pdf-recursive
cd markdown-pdf-recursive
pip install -e .
```

## Requirements

- Python 3.9+
- [Pandoc](https://pandoc.org/)
- A LaTeX engine for PDF generation (default: `xelatex`)

## Usage

```bash
MPRecursive ./vault --output vault.pdf --toc
```

## CLI flags

- `path` - Root directory to scan (positional)
- `-o, --output FILE` - Output PDF path
- `--toc` - Include table of contents
- `--sort name|modified|created` - File ordering mode
- `--include-images` - Reserved for future image strategy controls
- `--ignore FOLDER` - Ignore directory name (repeatable)
- `--verbose` - Print detailed conversion command
- `--engine pandoc` - Conversion engine selector
- `--pdf-engine ENGINE` - Pandoc PDF engine (default: `xelatex`)

## Examples

```bash
MPRecursive ./vault -o vault.pdf
MPRecursive ./notes --sort modified --toc -o notes.pdf
MPRecursive ./knowledge-base --ignore .git --ignore archive --verbose -o kb.pdf
```

## Termux usage

1. Install Python and Pandoc in Termux.
2. Install a TeX environment compatible with Pandoc PDF export.
3. Install MPRecursive:
   ```bash
   pip install markdown-pdf-recursive
   ```
4. Run:
   ```bash
   MPRecursive /sdcard/Documents/vault -o /sdcard/Documents/vault.pdf --toc
   ```

## Contribution guide

1. Fork the repository.
2. Create a feature branch.
3. Add/adjust tests for your change.
4. Run `pytest`.
5. Submit a pull request with clear rationale.

## Roadmap

- [x] Markdown → PDF
- [ ] HTML → PDF converter plugin
- [ ] DOCX → PDF converter plugin
- [ ] TXT → PDF converter plugin
- [ ] PDF → Markdown converter plugin
- [ ] PDF → Text converter plugin
- [ ] Markdown → HTML converter plugin
- [ ] Plugin discovery/registration system

## License

MIT License.


## Common Pandoc/Termux issues

- **YAML parse errors**: MPRecursive strips leading front matter from each file before merge, which avoids failures caused by malformed note properties.
- **`pdflatex`/`xelatex` not found**: install a TeX engine or run with another installed engine (for example `--pdf-engine=tectonic` if available).
- **Missing images**: ensure image links are relative to each note location or absolute valid paths.
