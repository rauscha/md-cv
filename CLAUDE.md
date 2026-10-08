# md-cv

## Purpose
Single-file CLI (`build_cv.py`) that turns a plain-text Markdown CV into a
styled `.docx` and `.pdf`. Source stays diffable in git; academic-CV
formatting (dated entries, lettered subsections, `[TBC]` scaffolding) is
handled by the parser/renderer instead of hand-formatting Word.

## Stack & setup
Python 3.11+, `python-docx` + `pypdf` (`requirements.txt`; `pywin32` entry is
Windows-only). Not a packaged library — just a script. On Linux, use `uv`:

```
uv venv .venv
uv pip install -r requirements.txt
```

PDF export needs an exporter: Word (Windows, via `pywin32`) or `soffice`
(LibreOffice), found via `PATH` or fallback paths in `_export_via_soffice`.
Neither is installed here — `apt install libreoffice` for local PDF export.

## Commands
- Build: `.venv/bin/python build_cv.py sample/Jane_Doe_CV.md [-o OUTDIR]` —
  Linux equivalent of `build.bat` (Windows drag-and-drop launcher, defaults
  to the Jane Doe sample with no file given).
- Tests: `uv run --with pytest pytest tests/` (pytest is not in
  `requirements.txt`/`.venv` — install it, don't add it to requirements
  without asking). Exporter-dependent tests self-skip when neither Word nor
  `soffice` is found (`_has_exporter()` in `tests/test_build_e2e.py`).

## Layout
- `build_cv.py` — parser, docx renderer, PDF export (Word COM or soffice
  subprocess), placeholder-leak check, CLI (`main()`); everything in one file.
- `sample/Jane_Doe_CV.md` — fictional example exercising every supported
  section; its built `.docx`/`.pdf` are committed alongside it.
- `tests/` — `test_parser.py`, `test_renderer.py`, `test_runs.py`,
  `test_export.py`, `test_placeholder.py`, `test_build_e2e.py`.
- `build.bat` — Windows-only launcher; irrelevant on Linux.

## Conventions & gotchas
- Layout follows the UChicago BSD/COAP CV template's *structure* (title block,
  labeled contact, caps headings, italic-underlined subsections, 1" date column,
  numbered citations, Name/Month Year/Page X of Y footer). Font is ours
  (Calibri), not the template's Arial — Andrew's call, 2026-10-08.
- Markdown grammar is fixed and documented in the README's format table —
  `# Name`, `Label: value` contact lines, `Dated: Place`, `## SECTION`,
  `### (a) Subsection`, `YYYY[-YYYY]|text` / `Current|text` dated entries,
  `Title | dates` heading lines, `1. ` numbered items, `- ` sub-bullets,
  indented `  - ` glyph bullets, `---` page break, `**bold**`/`*italic*`/
  `***both***`/`<u>underline</u>`, `[TBC]` to suppress a line or a whole
  heading's content. Don't loosen it without checking `tests/`.
- `--date YYYY-MM-DD` pins the CV date (default today); rebuilding on another
  day changes the dated line and footer, which shows up in the PDF diff.
- `private/` is gitignored: real people's CVs (e.g. the Romero COAP example
  used to build the template) live there, never in this public repo.
- `main()` exits 3, not argparse's 2, when a `[TBC]` placeholder leaks into
  the rendered PDF (2 is reserved for CLI usage errors).
- Style constants (fonts, sizes, indents) live at the top of `build_cv.py`.
- The CLI prints a diff of PDF text vs. the previous build as a sanity check.
