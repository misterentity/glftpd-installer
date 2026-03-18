@echo off
echo [*] glFTPd Installer GUI - [H4CK3R M0D3]
echo [*] Checking requirements...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo [*] Please install Python 3.6 or higher from https://www.python.org/downloads/
    echo [*] Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed!
    echo [*] Please install pip or reinstall Python
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "glftpd_installer_gui.py" (
    echo [ERROR] glftpd_installer_gui.py not found!
    echo [*] Please make sure you're in the correct directory
    pause
    exit /b 1
)

if not exist "install.sh" (
    echo [ERROR] install.sh not found!
    echo [*] Please make sure you're in the correct directory
    pause
    exit /b 1
)

REM Check and install requirements
echo [*] Checking Python packages...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install required packages!
    echo [*] Please check your internet connection and try again
    pause
    exit /b 1
)

echo [*] All requirements met!
echo [*] Starting GUI...
echo.

REM Start the GUI application
python glftpd_installer_gui.py

pause 