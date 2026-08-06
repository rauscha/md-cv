#!/usr/bin/env python3
"""Build a styled .docx and .pdf academic CV from a Markdown source.

Canonical home: https://github.com/rauscha/md-cv
Usage: python build_cv.py path/to/CV.md [-o OUTDIR]

Format: `# Name` then contact lines; `## SECTION`; `### (a) Subsection`;
dated entries as `2018-2021 | description` (must start with a 4-digit year);
everything else is a plain paragraph. `**bold**` / `*italic*` inline.
Lines containing [TBC] stay in the source but are stripped from output.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Entry:
    dates: str
    text: str


@dataclass
class Para:
    text: str


@dataclass
class Subsection:
    title: str
    items: list = field(default_factory=list)


@dataclass
class Section:
    title: str
    items: list = field(default_factory=list)


@dataclass
class CV:
    name: str
    contact: list
    sections: list


DATE_ENTRY_RE = re.compile(r"^(\d{4}[^|]*)\|(.*)$")


def parse_cv(text: str) -> CV:
    name = ""
    contact: list[str] = []
    sections: list[Section] = []
    section: Section | None = None
    sub: Subsection | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or "[TBC]" in line:
            continue
        if line.startswith("### "):
            if section is None:
                raise ValueError(
                    f"subsection before any '## SECTION' header: {line!r}"
                )
            sub = Subsection(line[4:].strip())
            section.items.append(sub)
        elif line.startswith("## "):
            section = Section(line[3:].strip())
            sub = None
            sections.append(section)
        elif line.startswith("# "):
            name = line[2:].strip()
        else:
            m = DATE_ENTRY_RE.match(line)
            item = Entry(m.group(1).strip(), m.group(2).strip()) if m else Para(line)
            if sub is not None:
                sub.items.append(item)
            elif section is not None:
                section.items.append(item)
            else:
                contact.append(line)
    return CV(name, contact, sections)


TOKEN_RE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)")


def tokenize_runs(text: str) -> list:
    out = []
    for part in TOKEN_RE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], True, False))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append((part[1:-1], False, True))
        else:
            out.append((part, False, False))
    return out
