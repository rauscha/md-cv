import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_cv import parse_cv, Entry, Para, Subsection

SAMPLE = """# Jane Doe, MD

Some University
Email: jane@example.edu

## ACADEMIC APPOINTMENTS

2018-2021 | Clinical Instructor, Some University
2021-present | Assistant Professor, Some University

## PUBLICATIONS

### (a) Peer-reviewed Publications

1. Doe J. A paper. *Journal*: 1-2. 2024
2020-2024 | This starts with a year and has a pipe

### (b) Book Chapters

## SCAFFOLD

Real line
Gather old talks [TBC]
"""


def test_name_and_contact():
    cv = parse_cv(SAMPLE)
    assert cv.name == "Jane Doe, MD"
    assert cv.contact == ["Some University", "Email: jane@example.edu"]


def test_sections_and_entries():
    cv = parse_cv(SAMPLE)
    s = cv.sections[0]
    assert s.title == "ACADEMIC APPOINTMENTS"
    assert s.items == [
        Entry("2018-2021", "Clinical Instructor, Some University"),
        Entry("2021-present", "Assistant Professor, Some University"),
    ]


def test_subsections_capture_following_items():
    cv = parse_cv(SAMPLE)
    pubs = cv.sections[1]
    sub_a, sub_b = pubs.items
    assert isinstance(sub_a, Subsection) and sub_a.title == "(a) Peer-reviewed Publications"
    assert sub_a.items[0] == Para("1. Doe J. A paper. *Journal*: 1-2. 2024")
    assert sub_a.items[1] == Entry("2020-2024", "This starts with a year and has a pipe")
    assert isinstance(sub_b, Subsection) and sub_b.items == []


def test_tbc_lines_stripped():
    cv = parse_cv(SAMPLE)
    scaffold = cv.sections[2]
    assert scaffold.items == [Para("Real line")]
