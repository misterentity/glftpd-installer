@echo off
echo [*] Starting glFTPd Installer GUI Tests...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.x and try again
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed
    echo Please install pip and try again
    pause
    exit /b 1
)

REM Install test requirements
echo [*] Installing test requirements...
pip install pytest pytest-cov >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install test requirements
    pause
    exit /b 1
)

REM Run tests with coverage
echo [*] Running tests...
python -m pytest test_gui.py -v --cov=glftpd_installer_gui --cov-report=term-missing

REM Check test results
if errorlevel 1 (
    echo.
    echo [ERROR] Some tests failed
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCESS] All tests passed
    echo [*] Coverage report has been generated
)

pause 