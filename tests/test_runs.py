import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_cv import tokenize_runs


def test_plain_text():
    assert tokenize_runs("Hello world") == [("Hello world", False, False, False)]


def test_bold_and_italic():
    assert tokenize_runs("**Doe J**, Smith A. *J Med*: 1-5. 2024") == [
        ("Doe J", True, False, False),
        (", Smith A. ", False, False, False),
        ("J Med", False, True, False),
        (": 1-5. 2024", False, False, False),
    ]


def test_lone_asterisk_left_alone():
    assert tokenize_runs("p < 0.05 * significant") == [("p < 0.05 * significant", False, False, False)]


def test_coauthor_asterisks_preserved():
    assert tokenize_runs("Doe J*, Smith A*, Jones B") == [
        ("Doe J*, Smith A*, Jones B", False, False, False)
    ]


def test_italic_adjacent_to_punctuation_still_works():
    assert tokenize_runs("*J Med*: 1-5") == [
        ("J Med", False, True, False),
        (": 1-5", False, False, False),
    ]


def test_bold_italic():
    assert tokenize_runs("***Nature***. 2010") == [
        ("Nature", True, True, False),
        (". 2010", False, False, False),
    ]


def test_underline_wraps_other_markup():
    assert tokenize_runs("Chen L, <u>Romero IL</u>, <u>**Doe J**</u>") == [
        ("Chen L, ", False, False, False),
        ("Romero IL", False, False, True),
        (", ", False, False, False),
        ("Doe J", True, False, True),
    ]
