# md-cv

## What this is

Keep your CV as a plain-text Markdown file; one command produces a formatted Word doc and PDF. Updating it stops being a Word-formatting chore — when a paper comes out, you just paste the citation into the file (or hand it to Claude or ChatGPT and say "add this paper"), run the build, and you're done. Because the source is plain text, it also plays nicely with git: every change to your CV is a readable diff, so you can see exactly what changed between versions, and nothing ever depends on the fragile internal formatting of a `.docx` file.

## See the sample

`sample/Jane_Doe_CV.md` is a complete, fictional example CV (Dr. Jane Doe, a made-up OB/GYN academic at a made-up "General Hospital") that exercises every section the tool supports — appointments, training, licensure, honors, clinical activities, funding, publications with lettered subsections, invited talks, and a statement section on its own page. The built outputs are committed alongside it so you can see the result without installing anything:

- [`sample/Jane_Doe_CV.md`](sample/Jane_Doe_CV.md) — the source
- [`sample/Jane_Doe_CV.docx`](sample/Jane_Doe_CV.docx) — the built Word document
- [`sample/Jane_Doe_CV.pdf`](sample/Jane_Doe_CV.pdf) — the built PDF

> **No-install option:** the same converter runs as a web drop-box at
> **cv.mfm.media** — verify with the access code (ask Andrew), drop your `.md`
> file, download the Word doc and PDF. Everything below is only needed if you
> want to build locally instead.

## Setup

1. Install **Python 3.11 or newer**, if you don't already have it.
2. From the project folder, install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. PDF export needs either **Microsoft Word** (on Windows) or **LibreOffice** (any operating system) installed. Word is used automatically if it's present; the tool falls back to LibreOffice otherwise.

## Build

```
python build_cv.py sample/Jane_Doe_CV.md
```

The `.docx` and `.pdf` land in the same folder as your Markdown file. To put them somewhere else, add `-o`:

```
python build_cv.py sample/Jane_Doe_CV.md -o build/
```

**Windows shortcut:** drag your `.md` file onto `build.bat` — no command line needed.

**On a Mac:** install [LibreOffice](https://www.libreoffice.org) (free — it handles the PDF export, since Word for Mac can't be driven by the script), then in Terminal, from this folder:

```
python3 build_cv.py My_CV.md
```

One note for Mac builds: if Microsoft Office isn't installed, LibreOffice substitutes a look-alike font for Calibri, so line breaks may shift slightly versus a Windows/Word build. The content is identical either way.

## Format reference

The layout follows the University of Chicago BSD CV format (the COAP template that circulates among senior faculty): a centered **CURRICULUM VITAE** title over your name, a labeled contact block, bold all-caps section headings, italic-underlined lettered subsections, dates in a one-inch left column, numbered citations, and a footer reading *Name — Month Year — Page X of Y* on every page.

| What you write | What you get |
|---|---|
| `# Jane Doe, MD` (first line) | **CURRICULUM VITAE** and your name, centered and bold at the top; your name also goes in the footer |
| `Dated: Springfield` (right after your name) | A right-aligned "Springfield, 10/8/26" line under your name, stamped with the build date (override with `--date YYYY-MM-DD`). The footer's month and year use the same date |
| `Address: General Hospital` | A contact line with the label in its own column and the value one inch in |
| Unlabeled lines after a labeled one | Continue that value (the rest of your address), lined up under it |
| `## PUBLICATIONS` | A section heading, bold and printed in capitals however you type it |
| `### (a) Peer-reviewed Publications` | A lettered subsection heading, italic and underlined |
| `2018-2021 \| Assistant Professor, ...` | A dated entry — the part before `\|` must start with a 4-digit year or the word `Current`; the date sits at the left margin and the description starts one inch in, with any wrapped lines hanging in that same column |
| `Current \| Society Name - Member` | A dated entry for an ongoing membership or role |
| `Grant name \| 2022-2024` | A heading line (text first, dates last): bold text with the dates right-aligned, as for a grant in **FUNDING**. Sub-bullets under it line up with it |
| `1. Doe J. Title. ***Journal***. 2024` | A numbered item with the number hanging to the left of the wrapped text, as for publications and abstracts |
| `- Designed a new curriculum` | A sub-bullet — indented to the text column of the line that introduces it (one inch in under a dated entry or a plain line, level with the title under a grant heading). No bullet glyph |
| `  - Hypertensive disorders` (indented) | A nested item with a bullet glyph, one step in from the description column (a clinical focus list under a dated entry) |
| `---` on its own line | Starts the next heading on a new page. The template begins each statement section (scholarly activity, clinical, education, citizenship) on a fresh page |
| `**Doe J**` / `*Journal*` / `***Journal***` | **Bold** / *italic* / ***bold italic*** text |
| `<u>Doe J</u>` | Underlined text, the template's convention for your own name in author lists |
| A plain line containing `[TBC]` | Kept in your source file as a personal reminder, but automatically left out of the Word doc and PDF — nothing marked `[TBC]` ever reaches the printed CV |
| `[TBC]` on a `##` or `###` heading, e.g. `## GRANTS & RESEARCH SUPPORT [TBC]` | Marks the whole section (or subsection) as a scaffold — a safe place to accumulate real, dated entries under it while you're still gathering material. The heading and everything under it (even non-`[TBC]` lines) are entirely left out of the Word doc and PDF until you remove `[TBC]` from the heading, at which point it prints normally |
| An empty `###` subsection (heading with nothing under it) | Prints as `None`, matching how empty subsections are conventionally shown on an academic CV |
| A blank line between two entries | Extra vertical space between them in the output (use it between publication citations, for example, so a run of papers doesn't read as one wall of text) |
| Any other line | A regular flush-left paragraph (used for sub-group labels like `(a) Didactic`, notes like `*co-first authors`, and statement text) |

## Updating with an AI assistant

Open your `.md` file in your editor of choice — it's just plain text, so nothing special is needed. Then tell Claude (or ChatGPT) what changed in plain English — for example, "add this paper, it was just accepted: \[paste citation]" — and let it edit the file for you. Rebuild with the one command, `python build_cv.py your_cv.md`, to regenerate the `.docx` and `.pdf`. Finally, review the diff the tool prints against your previous PDF, so you can confirm only the change you asked for actually changed before you send the new CV anywhere.
