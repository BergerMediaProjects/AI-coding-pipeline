@echo off
REM Double-click to start the AI Pipeline web interface (Windows)
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Please run setup first: double-click scripts\setup.bat
    echo Or install Docker and run: docker-compose up
    pause
    exit /b 1
)

start http://127.0.0.1:5001
.venv\Scripts\python.exe web_interface\app.py
pause
