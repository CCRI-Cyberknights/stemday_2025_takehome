#!/usr/bin/env python3
import os
import sys
import subprocess
import shlex

# === 🛠 CCRI STEM Day CTF Take-Home Setup Script (Non-Interactive) ===

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"
REPO_URL = "https://github.com/CCRI-Cyberknights/stemday2025_takehome.git"
REPO_DIR = os.path.expanduser("~/stemday2025_takehome")

APT_ENV = {
    **os.environ,
    "DEBIAN_FRONTEND": "noninteractive",
    "NEEDRESTART_SUSPEND": "1",       # avoid needrestart prompts
    "UCF_FORCE_CONFOLD": "1",         # keep existing config files
}

def run(cmd, check=True, env=None):
    """Run a shell command and show output, with non-interactive env by default."""
    if isinstance(cmd, str):
        print(f"💻 Running: {cmd}")
        rc = subprocess.run(cmd, shell=True, env=env or APT_ENV).returncode
    else:
        print(f"💻 Running: {' '.join(shlex.quote(c) for c in cmd)}")
        rc = subprocess.run(cmd, env=env or APT_ENV).returncode
    if check and rc != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)
    return rc

def apt_update():
    run(["sudo", "-E", "apt-get", "update", "-y"])

def apt_install(packages):
    print("📦 Installing system dependencies (non-interactive)...")
    apt_update()
    base = [
        "sudo", "-E", "apt-get", "install", "-yq",
        "-o", "Dpkg::Options::=--force-confdef",
        "-o", "Dpkg::Options::=--force-confold",
    ]
    run(base + packages)

def pip_install(packages):
    print("🐍 Installing Python packages...")
    run(["python3", "-m", "pip", "install", "--upgrade", "pip", "--break-system-packages"])
    run(["python3", "-m", "pip", "install", "--break-system-packages"] + packages)

def preseed_wireshark_and_install():
    """Preseed dumpcap setuid, install wireshark-common + tshark, reconfigure silently, add group."""
    print("🧪 Preseeding Wireshark (allow non-root capture) and installing non-interactively...")
    run("echo 'wireshark-common wireshark-common/install-setuid boolean true' | sudo debconf-set-selections")
    apt_install(["wireshark-common", "tshark"])
    run(["sudo", "dpkg-reconfigure", "-f", "noninteractive", "wireshark-common"])
    # Add invoking user to wireshark group (requires logout/login to take effect)
    target_user = os.environ.get("SUDO_USER") or os.environ.get("USER") or ""
    if target_user:
        run(["sudo", "usermod", "-aG", "wireshark", target_user])

def install_steghide_deb():
    print("🕵️ Checking Steghide version...")
    try:
        out = subprocess.check_output(["steghide", "--version"], text=True).strip()
        if "0.6.0" in out:
            print("✅ Steghide 0.6.0 already installed.")
            return
    except Exception:
        print("ℹ️ Steghide not found or outdated. Installing patched version...")

    apt_install(["wget"])
    print("⬇️ Downloading Steghide 0.6.0 .deb package...")
    run(["wget", "-q", STEGO_DEB_URL, "-O", "/tmp/steghide.deb"])

    print("📦 Installing patched Steghide (auto-fix deps if needed)...")
    rc = run("sudo dpkg -i /tmp/steghide.deb", check=False)
    if rc != 0:
        run([
            "sudo", "-E", "apt-get", "-f", "install", "-yq",
            "-o", "Dpkg::Options::=--force-confdef",
            "-o", "Dpkg::Options::=--force-confold",
        ])
    run("rm -f /tmp/steghide.deb")

    print("📌 Pinning Steghide 0.6.0 to prevent downgrade...")
    pin_contents = """Package: steghide
Pin: version 0.6.0*
Pin-Priority: 1001
"""
    with open("/tmp/steghide-pin", "w") as f:
        f.write(pin_contents)
    run(["sudo", "mv", "/tmp/steghide-pin", "/etc/apt/preferences.d/steghide"])

def install_zsteg():
    print("💎 Installing Ruby + zsteg (for image forensics)...")
    apt_install(["ruby", "ruby-dev", "libmagic-dev"])
    run(["sudo", "gem", "install", "zsteg", "--no-document"])

def clone_repo():
    if os.path.exists(REPO_DIR):
        print(f"ℹ️ Repository already exists at {REPO_DIR}")
        return
    print(f"🔁 Cloning the take-home CTF repository into {REPO_DIR} ...")
    apt_install(["git"])
    run(["git", "clone", REPO_URL, REPO_DIR])

def main():
    print("\n🚀 Setting up your CCRI STEM Day Take-Home environment...")
    print("=" * 60 + "\n")

    # Handle the known interactive offender first
    preseed_wireshark_and_install()

    apt_packages = [
        # Core & Python
        "python3", "python3-pip", "python3-venv",
        "gcc", "build-essential", "python3-markdown", "python3-scapy",

        # Challenge Tools
        "unzip", "lsof", "xdg-utils", "nmap", "hashcat",
        "qrencode", "libmcrypt4", "zbar-tools", "exiftool", "vim-common",
        "util-linux", "fonts-noto-color-emoji",

        # From challenge requirements
        "binwalk", "fcrackzip", "john", "radare2", "hexedit", "feh", "imagemagick"
    ]
    apt_install(apt_packages)

    install_steghide_deb()
    install_zsteg()
    pip_install(["flask", "markupsafe"])
    clone_repo()

    print("\n🎉 Setup complete!")
    print(f"📂 Your CTF folder is here: {REPO_DIR}")
    print("▶️ To start the CTF hub:")
    print(f"   cd {REPO_DIR} && python3 start_web_hub.py")
    print("ℹ️ If tshark non-root capture fails, log out/in once to apply wireshark group membership.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ This script may require sudo for installing system packages.")
    main()
