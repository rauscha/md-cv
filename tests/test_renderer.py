import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docx import Document

from build_cv import parse_cv, render_docx, INDENT, SPACE_GAP

MD = """# Jane Doe, MD

Email: jane@example.edu

## APPOINTMENTS

2021-present | Assistant Professor, **Some University**

## PUBLICATIONS

### (a) Peer-reviewed Publications

1. Doe J. A paper. *Journal*: 1-2. 2024

### (b) Book Chapters
"""


def build(tmp_path):
    out = tmp_path / "cv.docx"
    render_docx(parse_cv(MD), out)
    return Document(str(out))


def texts(doc):
    return [p.text for p in doc.paragraphs]


def test_structure_in_order(tmp_path):
    t = texts(build(tmp_path))
    assert t[0] == "Jane Doe, MD"
    assert "APPOINTMENTS" in t
    assert "2021-present\tAssistant Professor, Some University" in t
    assert "(a) Peer-reviewed Publications" in t


def test_dated_entry_hanging_indent(tmp_path):
    doc = build(tmp_path)
    p = next(p for p in doc.paragraphs if p.text.startswith("2021-present\t"))
    pf = p.paragraph_format
    assert pf.left_indent == INDENT
    assert pf.first_line_indent == -INDENT
    assert pf.tab_stops[0].position == INDENT


def test_bold_italic_runs(tmp_path):
    doc = build(tmp_path)
    entry = next(p for p in doc.paragraphs if "Some University" in p.text)
    assert any(r.bold and r.text == "Some University" for r in entry.runs)
    cite = next(p for p in doc.paragraphs if p.text.startswith("1. Doe J"))
    assert any(r.italic and r.text == "Journal" for r in cite.runs)


def test_empty_subsection_renders_none(tmp_path):
    t = texts(build(tmp_path))
    i = t.index("(b) Book Chapters")
    assert t[i + 1] == "None"


def test_name_is_large_bold(tmp_path):
    doc = build(tmp_path)
    run = doc.paragraphs[0].runs[0]
    assert run.bold
    assert run.font.size.pt > 12


def test_gap_renders_empty_paragraph(tmp_path):
    out = tmp_path / "gap.docx"
    render_docx(parse_cv("## PUBS\n\nDoe J. One. 2024\n\nDoe J. Two. 2023\n"), out)
    doc = Document(str(out))
    gapped = next(p for p in doc.paragraphs if p.text == "Doe J. One. 2024")
    assert gapped.paragraph_format.space_after == SPACE_GAP
