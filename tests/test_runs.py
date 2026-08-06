import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_cv import tokenize_runs


def test_plain_text():
    assert tokenize_runs("Hello world") == [("Hello world", False, False)]


def test_bold_and_italic():
    assert tokenize_runs("**Doe J**, Smith A. *J Med*: 1-5. 2024") == [
        ("Doe J", True, False),
        (", Smith A. ", False, False),
        ("J Med", False, True),
        (": 1-5. 2024", False, False),
    ]


def test_lone_asterisk_left_alone():
    assert tokenize_runs("p < 0.05 * significant") == [("p < 0.05 * significant", False, False)]
