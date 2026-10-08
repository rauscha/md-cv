import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_cv import parse_cv, Bullet, Entry, Heading, Nested, Numbered, PageBreak, Para, Subsection

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
    assert sub_a.items[0] == Numbered("1", "Doe J. A paper. *Journal*: 1-2. 2024")
    assert sub_a.items[1] == Entry("2020-2024", "This starts with a year and has a pipe")
    assert isinstance(sub_b, Subsection) and sub_b.items == []


def test_tbc_lines_stripped():
    cv = parse_cv(SAMPLE)
    scaffold = cv.sections[2]
    assert scaffold.items == [Para("Real line")]


def test_subsection_before_section_raises_clear_error():
    with pytest.raises(ValueError, match="subsection before any '## SECTION' header"):
        parse_cv("# Name\n\n### (a) Orphan subsection\n")


def test_current_dated_entry():
    cv = parse_cv("## MEMBERSHIPS\n\nCurrent | Some Society - Member\n")
    assert cv.sections[0].items == [Entry("Current", "Some Society - Member")]


def test_blank_line_between_items_sets_gap():
    cv = parse_cv("## PUBS\n\nDoe J. Paper one. 2024\n\nDoe J. Paper two. 2023\n")
    first, second = cv.sections[0].items
    assert first.gap is True
    assert second.gap is False


def test_no_gap_when_items_adjacent():
    cv = parse_cv("## JOBS\n\n2020-2021 | A\n2021-2022 | B\n")
    assert [e.gap for e in cv.sections[0].items] == [False, False]


def test_blank_after_header_creates_no_gap():
    cv = parse_cv("## PUBS\n\n### (a) Papers\n\nDoe J. Paper. 2024\n")
    sub = cv.sections[0].items[0]
    assert sub.items[0].gap is False


def test_dash_line_becomes_sub_bullet():
    cv = parse_cv(
        "## TEACHING ACTIVITIES\n"
        "Residency, Some University\n"
        "- Designed a new ultrasound curriculum\n"
        "- Annual didactics: Embryology\n"
    )
    items = cv.sections[0].items
    assert items == [
        Para("Residency, Some University"),
        Bullet("Designed a new ultrasound curriculum"),
        Bullet("Annual didactics: Embryology"),
    ]


def test_sub_bullet_inside_subsection():
    cv = parse_cv("## TEACHING\n\n### (a) Courses\n\n- One course\n")
    sub = cv.sections[0].items[0]
    assert sub.items == [Bullet("One course")]


def test_sub_bullet_takes_gap_from_blank_line():
    cv = parse_cv("## TEACHING\n\n- First\n\nNext block\n")
    first, second = cv.sections[0].items
    assert first == Bullet("First", gap=True)
    assert second == Para("Next block")


def test_tbc_header_creates_scaffold_section():
    cv = parse_cv("## REAL\n\n2020 | A\n\n## GRANTS [TBC]\n\n2021 | Real grant entry\n")
    real, grants = cv.sections
    assert real.scaffold is False
    assert grants.scaffold is True
    assert grants.items == [Entry("2021", "Real grant entry")]
    assert real.items == [Entry("2020", "A")]  # nothing misfiled


def test_text_then_dates_is_a_heading_line():
    cv = parse_cv("## FUNDING\n\nNIH K12 Scholar | 2009-2016\n- Role: PI\nOld grant | 2007-\n")
    assert cv.sections[0].items == [
        Heading("NIH K12 Scholar", "2009-2016"), Bullet("Role: PI"), Heading("Old grant", "2007-"),
    ]


def test_pipe_with_trailing_prose_is_not_a_heading():
    cv = parse_cv("## X\n\nFoo | 2021 something else\n")
    assert cv.sections[0].items == [Para("Foo | 2021 something else")]


def test_indented_dash_is_nested_item():
    cv = parse_cv("## CLINICAL\n\n2007- | Practice:\n  - Focus one\n- Plain bullet\n")
    assert cv.sections[0].items == [
        Entry("2007-", "Practice:"), Nested("Focus one"), Bullet("Plain bullet"),
    ]


def test_rule_is_page_break():
    cv = parse_cv("## A\n\nText\n\n---\n## B\n")
    assert cv.sections[0].items == [Para("Text", gap=True), PageBreak()]
