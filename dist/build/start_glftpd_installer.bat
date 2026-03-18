@echo off
python start_glftpd_installer.py
if errorlevel 1 (
    echo Error launching application
    pause
)
