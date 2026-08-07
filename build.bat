@echo off
rem Builds a Word doc + PDF from a Markdown CV.
rem Easiest use: drag your .md file onto this build.bat icon.
rem Double-clicking with no file builds the Jane Doe sample as a demo.
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install it from python.org ^(check "Add to PATH"^), then try again.
  pause
  exit /b 1
)
python -m pip install -r "%~dp0requirements.txt" --quiet
if "%~1"=="" (
  python "%~dp0build_cv.py" "%~dp0sample\Jane_Doe_CV.md"
) else (
  python "%~dp0build_cv.py" "%~1"
)
echo.
pause
