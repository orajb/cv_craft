@echo off
REM CV Crafter - Windows Launcher
REM Usage: Double-click run.bat or run from command prompt

echo.
echo 🎯 CV Crafter - AI-Powered CV Generator
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo ✓ Python found

REM Create venv if needed
if not exist "venv" (
    echo → Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate venv
call venv\Scripts\activate.bat

REM Always sync dependencies (pip is fast when packages already installed)
echo → Checking dependencies...
pip install --upgrade pip -q 2>nul
pip install -r requirements.txt -q 2>nul
echo ✓ Dependencies ready

REM Create data directory
if not exist "data" mkdir data

echo.
echo 🚀 Starting CV Crafter...
echo    Opening in your browser at http://localhost:8501
echo    Press Ctrl+C to stop
echo.

streamlit run app.py --server.headless=true
