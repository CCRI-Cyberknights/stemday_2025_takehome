#!/usr/bin/env python3
import os
import sys
import subprocess

# === 🛠 CCRI STEM Day CTF Take-Home Setup Script ===

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"
REPO_URL = "https://github.com/CCRI-Cyberknights/stemday2025_takehome.git"
REPO_DIR = os.path.expanduser("~/stemday2025_takehome")

def run(cmd, check=True):
    """Run a shell command and show output."""
    print(f"💻 Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)

def apt_install(packages):
    print("📦 Installing system dependencies...")
    run("sudo apt update -y")
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
    run(f"wget -q {STEGO_DEB_URL} -O /tmp/steghide.deb")

    print("📦 Installing patched Steghide...")
    run("sudo dpkg -i /tmp/steghide.deb || sudo apt --fix-broken install -y")
    run("rm /tmp/steghide.deb")

    print("📌 Pinning Steghide 0.6.0 to prevent downgrade...")
    pin_contents = """Package: steghide
Pin: version 0.6.0*
Pin-Priority: 1001
"""
    with open("/tmp/steghide-pin", "w") as f:
        f.write(pin_contents)
    run("sudo mv /tmp/steghide-pin /etc/apt/preferences.d/steghide")

def install_zsteg():
    print("💎 Installing Ruby + zsteg (for image forensics)...")
    run("sudo apt install -y ruby ruby-dev libmagic-dev")
    run("sudo gem install zsteg")

def clone_repo():
    if os.path.exists(REPO_DIR):
        print(f"ℹ️ Repository already exists at {REPO_DIR}")
        return
    print(f"🔁 Cloning the take-home CTF repository into {REPO_DIR} ...")
    run(f"git clone {REPO_URL} {REPO_DIR}")

def main():
    print("\n🚀 Setting up your CCRI STEM Day Take-Home environment...")
    print("=" * 60 + "\n")

    apt_packages = [
        # Core & Python
        "git", "python3", "python3-pip", "python3-venv",
        "gcc", "build-essential", "python3-markdown", "python3-scapy",

        # Challenge Tools
        "unzip", "lsof", "xdg-utils", "nmap", "tshark", "hashcat",
        "qrencode", "libmcrypt4", "zbar-tools", "exiftool", "vim-common",
        "util-linux", "fonts-noto-color-emoji",

        # From challenge requirements
        "binwalk", "fcrackzip", "john", "radare2", "hexedit", "feh", "imagemagick"
    ]
    apt_install(apt_packages)
    install_steghide_deb()
    install_zsteg()

    pip_packages = ["flask", "markupsafe"]
    pip_install(pip_packages)

    clone_repo()

    print("\n🎉 Setup complete!")
    print(f"📂 Your CTF folder is here: {REPO_DIR}")
    print("▶️ To start the CTF hub:")
    print(f"   cd {REPO_DIR} && python3 start_web_hub.py")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ This script may require sudo for installing system packages.")
    main()
