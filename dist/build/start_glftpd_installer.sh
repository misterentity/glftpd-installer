#!/bin/bash
python3 start_glftpd_installer.py
if [ $? -ne 0 ]; then
    echo "Error launching application"
    read -p "Press Enter to exit..."
fi
