#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    # Check if requirements are installed
    try:
        print("Checking requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Requirements satisfied.")
    except subprocess.CalledProcessError:
        print("Error installing requirements. Please run: pip install -r requirements.txt")
        input("Press Enter to exit...")
        return
    
    # Start the application
    print("Starting glFTPd Installer GUI...")
    subprocess.run([sys.executable, "glftpd_installer_gui.py"])

if __name__ == "__main__":
    main()
