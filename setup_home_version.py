#!/usr/bin/env python3
import os
import sys
import subprocess

# === 🛠 CCRI STEM Day CTF Take-Home Setup Script ===

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"

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
    run("python3 -m pip install --upgrade pip --break-system-packages")
    run(f"python3 -m pip install --break-system-packages {' '.join(packages)}")

def install_steghide_deb():
    print("🕵️ Checking Steghide version...")
    try:
        version_output = subprocess.check_output(["steghide", "--version"], text=True).strip()
        if "0.6.0" in version_output:
            print("✅ Steghide 0.6.0 already installed.")
            return
    except Exception:
        print("ℹ️ Steghide not found or outdated. Installing patched version...")

    print("⬇️ Downloading Steghide 0.6.0 .deb package...")
    run(["wget", "-q", STEGO_DEB_URL, "-O", "/tmp/steghide.deb"])

    print("📦 Installing patched Steghide...")
    run("sudo dpkg -i /tmp/steghide.deb || sudo apt --fix-broken install -y")
    run("rm /tmp/steghide.deb")

    print("📌 Pinning Steghide 0.6.0 to prevent downgrade...")
    pin_file = "/etc/apt/preferences.d/steghide"
    pin_contents = """Package: steghide
Pin: version 0.6.0*
Pin-Priority: 1001
"""
    with open("/tmp/steghide-pin", "w") as f:
        f.write(pin_contents)
    run(["sudo", "mv", "/tmp/steghide-pin", pin_file])

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
        "nmap", "tshark", "hashcat", "qrencode",
        "zbar-tools", "exiftool", "vim-common", "util-linux",
        "python3-markdown", "python3-scapy"
    ]
    apt_install(apt_packages)

    # === Install patched Steghide ===
    install_steghide_deb()

    # === Install Python libraries ===
    pip_packages = ["flask", "markupsafe"]
    pip_install(pip_packages)

    # === Clone the take-home repo ===
    clone_repo()

    print("\n🎉 Setup complete! You can now launch the CTF from:")
    print("   ~/stemday2025_takehome/start_web_hub.py")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ This script may require sudo for installing system packages.")
    main()
