import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_cv

MD = """# Jane Doe, MD

Email: jane@example.edu

## APPOINTMENTS

2021-present | Assistant Professor
Old job to confirm [TBC]
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


@pytest.mark.skipif(not _has_exporter(), reason="no Word or LibreOffice available")
def test_end_to_end_build(tmp_path, capsys):
    md = tmp_path / "cv.md"
    md.write_text(MD, encoding="utf-8")
    build_cv.main([str(md)])
    assert (tmp_path / "cv.docx").exists()
    pdf = tmp_path / "cv.pdf"
    assert pdf.exists()
    text, pages = build_cv.extract_pdf_text(pdf)
    assert "Jane Doe" in text
    assert "TBC" not in text
    assert pages >= 1
    assert "Built" in capsys.readouterr().out
