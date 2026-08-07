import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_cv


def test_soffice_profile_dir_flag_present_when_given(tmp_path, monkeypatch):
    """A per-request profile dir must be passed as the *first* soffice argument,
    matching converter/server.js's `-env:UserInstallation=file://{profile}` flag,
    so headless soffice doesn't corrupt state across concurrent requests."""
    recorded = {}

    def fake_run(cmd, **kwargs):
        recorded["cmd"] = cmd
        raise build_cv.subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(build_cv.shutil, "which", lambda name: "soffice")
    monkeypatch.setattr(build_cv.subprocess, "run", fake_run)

    docx = tmp_path / "cv.docx"
    pdf = tmp_path / "cv.pdf"
    profile = tmp_path / "lo-profile"

    build_cv._export_via_soffice(docx, pdf, profile_dir=profile)

    cmd = recorded["cmd"]
    assert cmd[0] == "soffice"
    assert cmd[1] == f"-env:UserInstallation=file://{profile}"
    assert cmd[2:] == [
        "--headless", "--convert-to", "pdf",
        "--outdir", str(pdf.parent), str(docx),
    ]


def test_soffice_no_profile_dir_flag_when_absent(tmp_path, monkeypatch):
    """Default (profile_dir=None) must leave the owner's existing Windows/Word-
    adjacent LibreOffice invocation byte-for-byte unchanged."""
    recorded = {}

    def fake_run(cmd, **kwargs):
        recorded["cmd"] = cmd
        raise build_cv.subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(build_cv.shutil, "which", lambda name: "soffice")
    monkeypatch.setattr(build_cv.subprocess, "run", fake_run)

    docx = tmp_path / "cv.docx"
    pdf = tmp_path / "cv.pdf"

    build_cv._export_via_soffice(docx, pdf)

    cmd = recorded["cmd"]
    assert not any(str(arg).startswith("-env:UserInstallation=") for arg in cmd)
    assert cmd == [
        "soffice", "--headless", "--convert-to", "pdf",
        "--outdir", str(pdf.parent), str(docx),
    ]


def test_export_pdf_forwards_profile_dir_to_soffice(tmp_path, monkeypatch):
    """export_pdf's profile_dir must reach _export_via_soffice; the Word path
    (tried first) is untouched and unaffected by this parameter."""
    monkeypatch.setattr(build_cv, "_export_via_word", lambda *a, **k: False)

    recorded = {}

    def fake_soffice(docx_path, pdf_path, profile_dir=None):
        recorded["profile_dir"] = profile_dir
        return True

    monkeypatch.setattr(build_cv, "_export_via_soffice", fake_soffice)

    docx = tmp_path / "cv.docx"
    pdf = tmp_path / "cv.pdf"
    profile = tmp_path / "lo-profile"

    engine = build_cv.export_pdf(docx, pdf, profile_dir=profile)

    assert engine == "libreoffice"
    assert recorded["profile_dir"] == profile


def test_main_forwards_profile_dir_flag_to_export_pdf(tmp_path, monkeypatch):
    """`--profile-dir` on the CLI must reach export_pdf(), so a server invoking
    build_cv.py as a subprocess can give each request its own LibreOffice profile
    (see converter/server.js's -env:UserInstallation usage upstream)."""
    md = tmp_path / "cv.md"
    md.write_text("# Jane Doe\n\nEmail: jane@example.edu\n", encoding="utf-8")

    recorded = {}

    def fake_export_pdf(docx_path, pdf_path, profile_dir=None):
        recorded["profile_dir"] = profile_dir
        pdf_path.write_bytes(b"%PDF-fake")
        return "libreoffice"

    monkeypatch.setattr(build_cv, "export_pdf", fake_export_pdf)
    monkeypatch.setattr(build_cv, "extract_pdf_text", lambda path: ("Jane Doe", 1))

    profile = tmp_path / "lo-profile"
    build_cv.main([str(md), "--profile-dir", str(profile)])

    assert recorded["profile_dir"] == profile


def test_main_no_profile_dir_flag_defaults_to_none(tmp_path, monkeypatch):
    """Omitting `--profile-dir` must leave the owner's existing Windows/Word CLI
    invocation unchanged: export_pdf() gets profile_dir=None, same as before this
    flag existed."""
    md = tmp_path / "cv.md"
    md.write_text("# Jane Doe\n\nEmail: jane@example.edu\n", encoding="utf-8")

    recorded = {}

    def fake_export_pdf(docx_path, pdf_path, profile_dir=None):
        recorded["profile_dir"] = profile_dir
        pdf_path.write_bytes(b"%PDF-fake")
        return "word"

    monkeypatch.setattr(build_cv, "export_pdf", fake_export_pdf)
    monkeypatch.setattr(build_cv, "extract_pdf_text", lambda path: ("Jane Doe", 1))

    build_cv.main([str(md)])

    assert recorded["profile_dir"] is None
