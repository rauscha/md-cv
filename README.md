# md-cv

## What this is

Keep your CV as a plain-text Markdown file; one command produces a formatted Word doc and PDF. Updating it stops being a Word-formatting chore — when a paper comes out, you just paste the citation into the file (or hand it to Claude or ChatGPT and say "add this paper"), run the build, and you're done. Because the source is plain text, it also plays nicely with git: every change to your CV is a readable diff, so you can see exactly what changed between versions, and nothing ever depends on the fragile internal formatting of a `.docx` file.

## See the sample

`sample/Jane_Doe_CV.md` is a complete, fictional example CV (Dr. Jane Doe, a made-up OB/GYN academic at a made-up "General Hospital") that exercises every section the tool supports — appointments, training, licensure, honors, publications with lettered subsections, invited talks. The built outputs are committed alongside it so you can see the result without installing anything:

- [`sample/Jane_Doe_CV.md`](sample/Jane_Doe_CV.md) — the source
- [`sample/Jane_Doe_CV.docx`](sample/Jane_Doe_CV.docx) — the built Word document
- [`sample/Jane_Doe_CV.pdf`](sample/Jane_Doe_CV.pdf) — the built PDF

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

## Format reference

| What you write | What you get |
|---|---|
| `# Jane Doe, MD` (first line) | Your name, printed large and bold at the top |
| Plain lines right after your name | Contact info (address, email, phone) |
| `## PUBLICATIONS` | A section heading |
| `### (a) Peer-reviewed Publications` | A lettered subsection heading inside a section |
| `2018-2021 \| Assistant Professor, ...` | A dated entry — the part before `\|` must start with a 4-digit year or the word `Current`; the date sits at the left margin and the description starts in its own column 1.15 inches in, with any wrapped lines hanging in that same column |
| `Current \| Society Name - Member` | A dated entry for an ongoing membership or role — same column layout as a year-dated entry, for things that don't have an end date |
| `- Designed a new curriculum` | A sub-bullet — the whole line is indented to the 1.15-inch description column, so a run of them lines up underneath the plain line that introduces them (used for the activities listed under a teaching or clinical heading) |
| `**Doe J**` | **Bold** text |
| `*Journal Name*` | *Italic* text |
| A plain line containing `[TBC]` | Kept in your source file as a personal reminder, but automatically left out of the Word doc and PDF — nothing marked `[TBC]` ever reaches the printed CV |
| `[TBC]` on a `##` or `###` heading, e.g. `## GRANTS & RESEARCH SUPPORT [TBC]` | Marks the whole section (or subsection) as a scaffold — a safe place to accumulate real, dated entries under it while you're still gathering material. The heading and everything under it (even non-`[TBC]` lines) are entirely left out of the Word doc and PDF until you remove `[TBC]` from the heading, at which point it prints normally |
| An empty `###` subsection (heading with nothing under it) | Prints as `None`, matching how empty subsections are conventionally shown on an academic CV |
| A blank line between two entries | Extra vertical space between them in the output (use it between publication citations, for example, so a run of papers doesn't read as one wall of text) |
| Any other line — no leading `year \|` / `Current \|` and no `#` heading markers | A regular flush-left paragraph, not indented like a dated entry (used for contact lines, numbered citations, and notes like `*co-first authors`) |

## Updating with an AI assistant

Open your `.md` file in your editor of choice — it's just plain text, so nothing special is needed. Then tell Claude (or ChatGPT) what changed in plain English — for example, "add this paper, it was just accepted: \[paste citation]" — and let it edit the file for you. Rebuild with the one command, `python build_cv.py your_cv.md`, to regenerate the `.docx` and `.pdf`. Finally, review the diff the tool prints against your previous PDF, so you can confirm only the change you asked for actually changed before you send the new CV anywhere.
