import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_cv

# Bare "TBC" (no brackets) survives parse_cv's `[TBC]`-line-stripping and
# actually reaches the rendered PDF text -- the case a non-technical colleague
# hits by mistyping the sample's placeholder convention.
MD_WITH_LEAK = """# Jane Doe, MD

Email: jane@example.edu

## APPOINTMENTS

2021-present | TBC pending confirmation
"""

MD_CLEAN = """# Jane Doe, MD

Email: jane@example.edu

## APPOINTMENTS

2021-present | Assistant Professor
"""


def _has_exporter():
    try:
        import win32com.client  # noqa: F401
        return True
    except ImportError:
        pass
    return bool(
        shutil.which("soffice")
        or Path(r"C:\Program Files\LibreOffice\program\soffice.exe").exists()
    )


def test_check_for_placeholders_raises_on_leaked_text():
    with pytest.raises(build_cv.PlaceholderError):
        build_cv.check_for_placeholders("2021-present\tTBC pending confirmation")


def test_check_for_placeholders_passes_clean_text():
    build_cv.check_for_placeholders("2021-present\tAssistant Professor")  # no raise


@pytest.mark.skipif(not _has_exporter(), reason="no Word or LibreOffice available")
def test_cli_exits_2_with_message_on_placeholder_leak(tmp_path, capsys):
    md = tmp_path / "cv.md"
    md.write_text(MD_WITH_LEAK, encoding="utf-8")
    try:
        with pytest.raises(SystemExit) as exc_info:
            build_cv.main([str(md)])
    except RuntimeError as exc:
        pytest.skip(f"no usable PDF exporter at runtime: {exc}")
    assert exc_info.value.code == 2
    assert "ERROR: [TBC] content leaked into the PDF" in capsys.readouterr().err


@pytest.mark.skipif(not _has_exporter(), reason="no Word or LibreOffice available")
def test_cli_exits_cleanly_for_clean_cv(tmp_path):
    md = tmp_path / "cv.md"
    md.write_text(MD_CLEAN, encoding="utf-8")
    try:
        build_cv.main([str(md)])  # must not raise
    except RuntimeError as exc:
        pytest.skip(f"no usable PDF exporter at runtime: {exc}")
