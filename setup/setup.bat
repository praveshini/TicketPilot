@echo off
setlocal
echo Initializing environment setup for Windows...

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not detected in the system PATH.
    exit /b 1
)

:: Create virtual environment
if not exist venv (
    python -m venv venv
    echo Created virtual environment: venv
)

:: Activate environment and update pip
call venv\Scripts\activate
python -m pip install --upgrade pip

:: Install dependencies
if exist requirements.txt (
    pip install -r requirements.txt
    echo Dependencies successfully installed.
) else (
    echo Warning: requirements.txt not detected. Skipping installation.
)

echo Setup finalized. Activate the environment with: venv\Scripts\activate
pause