#!/usr/bin/env python3
import os
import sys
import shutil
import zipfile
from pathlib import Path

DIST_FILES = [
    "glftpd_installer_gui.py",
    "requirements.txt",
    "README.MD",
]


def create_distribution():
    """Create a production-ready distribution package."""
    print("Creating glFTPd Installer GUI distribution package...")

    dist_dir = Path("dist")
    build_dir = dist_dir / "build"

    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    build_dir.mkdir(parents=True)

    missing = [f for f in DIST_FILES if not Path(f).exists()]
    if "requirements.txt" in missing:
        Path("requirements.txt").write_text("paramiko==3.4.0\n")
        missing.remove("requirements.txt")
        print("Created requirements.txt")

    if missing:
        print(f"Error: Missing required files: {', '.join(missing)}")
        sys.exit(1)

    for f in DIST_FILES:
        shutil.copy(f, build_dir)

    (build_dir / "start_glftpd_installer.py").write_text("""\
#!/usr/bin/env python3
import subprocess, sys

def main():
    try:
        print("Checking requirements...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Requirements satisfied.")
    except subprocess.CalledProcessError:
        print("Error installing requirements. "
              "Please run: pip install -r requirements.txt")
        input("Press Enter to exit...")
        return

    print("Starting glFTPd Installer GUI...")
    subprocess.run([sys.executable, "glftpd_installer_gui.py"])

if __name__ == "__main__":
    main()
""")

    (build_dir / "start_glftpd_installer.bat").write_text("""\
@echo off
python start_glftpd_installer.py
if errorlevel 1 (
    echo Error launching application
    pause
)
""")

    sh_script = build_dir / "start_glftpd_installer.sh"
    sh_script.write_text("""\
#!/bin/bash
python3 start_glftpd_installer.py
if [ $? -ne 0 ]; then
    echo "Error launching application"
    read -p "Press Enter to exit..."
fi
""")
    os.chmod(sh_script, 0o755)

    zip_path = dist_dir / "glftpd_installer_gui.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in build_dir.glob("**/*"):
            if f.is_file():
                zf.write(f, f.relative_to(build_dir))

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Distribution package created: {zip_path}")
    print(f"Size: {size_mb:.2f} MB")
    return zip_path


if __name__ == "__main__":
    create_distribution()
