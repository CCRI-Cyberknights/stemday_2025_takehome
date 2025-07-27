#!/usr/bin/env python3
import os
import sys
import subprocess

# === 🛠 CCRI STEM Day CTF Take-Home Setup Script ===

def run(cmd, check=True):
    print(f"💻 Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)

def apt_install(packages):
    print("📦 Installing system dependencies...")
    run("sudo apt update")
    run(f"sudo apt install -y {' '.join(packages)}")

def pip_install(packages):
    print("🐍 Installing Python packages...")
    run("python3 -m pip install --upgrade pip")
    run(f"python3 -m pip install {' '.join(packages)}")

def clone_repo():
    print("🔁 Cloning the take-home CTF repository...")
    run("git clone https://github.com/CCRI-Cyberknights/stemday2025_takehome.git")

def main():
    print("\n🚀 Setting up your CCRI STEM Day Take-Home environment...")
    print("=" * 60 + "\n")

    # === Install system dependencies ===
    apt_packages = [
        "git", "python3", "python3-pip", "python3-venv",
        "gcc", "build-essential", "unzip", "lsof", "xdg-utils",
        "nmap", "tshark", "steghide", "hashcat", "qrencode",
        "zbar-tools", "exiftool", "vim-common", "util-linux",
        "python3-markdown", "python3-scapy"
    ]
    apt_install(apt_packages)

    # === Install Python libraries ===
    pip_packages = ["flask", "markupsafe"]
    pip_install(pip_packages)

    # === Clone the take-home repo ===
    clone_repo()

    print("\n🎉 Setup complete! You can now launch the CTF from:")
    print("   ~/stemday2025_takehome/start_web_hub.py")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  This script may require sudo for installing system packages.")
    main()
