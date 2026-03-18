# Project Brief: glFTPd Installer GUI

## Purpose
A Python/Tkinter GUI application that configures and deploys glFTPd (an FTP daemon) on remote Linux servers via SSH. Wraps the existing shell-based `install.sh` installer with a graphical interface.

## Core Features
- SSH connection management (connect to remote Linux server)
- GUI form for all installation parameters (site config, IRC, sections, optional scripts, admin account)
- Generate `install.cache` configuration files for unattended installation
- Transfer files and execute remote installation via SSH/SFTP
- Export offline installer packages (zip with install.sh + install.cache)
- Real-time installation log with progress tracking

## Target Platform
- GUI runs on Windows (also works on Linux/macOS)
- Installs to remote Debian/Slackware Linux servers

## Tech Stack
- Python 3.6+, Tkinter, paramiko (SSH), threading
- Cyberpunk-themed dark UI (Consolas font, green-on-black)
