@echo off
REM Quick setup script for researchers (Windows)
REM Double-click or run from project root: scripts\setup.bat

cd /d "%~dp0.."

echo === AI Pipeline Setup ===

REM Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is required. Install from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    copy .env.example .env
    echo Created .env from .env.example
    echo You can add your OPENAI_API_KEY to .env, or enter it in the web interface.
) else (
    echo .env already exists
)

REM Generate sample data if needed
if not exist "data\training_data_sample.xlsx" (
    echo Generating sample data...
    python scripts\generate_sample_data.py
)

echo.
echo === Setup complete ===
echo Next steps:
echo   1. Double-click start.bat to launch the web interface
echo   2. Or run: python web_interface\app.py
echo   3. Open http://127.0.0.1:5001 in your browser
echo   4. Enter your API key in the web form when prompted
echo.
pause
