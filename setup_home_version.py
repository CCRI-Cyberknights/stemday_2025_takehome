#!/usr/bin/env python3
import os
import sys
import subprocess
import shlex
import argparse
import shutil
import stat

# === 🛠 CCRI STEM Day CTF Take-Home Setup Script (Parrot-aware; Live-CD aware) ===

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"
REPO_URL = "https://github.com/CCRI-Cyberknights/stemday2025_takehome.git"
REPO_DIR = os.path.expanduser("~/stemday2025_takehome")

APT_ENV = {
    **os.environ,
    "DEBIAN_FRONTEND": "noninteractive",
    "NEEDRESTART_SUSPEND": "1",
    "UCF_FORCE_CONFOLD": "1",
}

# -----------------------------
# Live-CD / privilege helpers
# -----------------------------
def is_root() -> bool:
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def is_live() -> bool:
    # Parrot/Debian live indicators
    try:
        if os.path.exists("/lib/live/mount/medium") or os.path.exists("/run/live/medium"):
            return True
        with open("/proc/cmdline", "r") as f:
            s = f.read()
        return "boot=live" in s
    except Exception:
        return False

def need_sudo_prefix() -> bool:
    # In a live session we avoid sudo entirely and expect root
    if is_live():
        return False
    return not is_root()

def sudo_prefix_list():
    if need_sudo_prefix():
        if shutil.which("sudo") is None:
            sys.exit("This script needs root privileges. Re-run as: sudo -E python3 script.py")
        return ["sudo", "-E"]
    return []

def run(cmd, check=True, env=None):
    """Run a command list or string; auto-add sudo for lists when appropriate."""
    if isinstance(cmd, str):
        # For shell pipelines, prefer run_shell() so we can sudo-wrap cleanly.
        print(f"💻 Running (shell): {cmd}")
        rc = subprocess.run(cmd, shell=True, env=env or APT_ENV).returncode
    else:
        if len(cmd) > 0 and cmd[0] not in ("sudo", "pkexec") and need_sudo_prefix():
            cmd = sudo_prefix_list() + list(cmd)
        print(f"💻 Running: {' '.join(shlex.quote(c) for c in cmd)}")
        rc = subprocess.run(cmd, env=env or APT_ENV).returncode
    if check and rc != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)
    return rc

def run_shell(cmd_str: str, check=True, env=None):
    """Run a bash -lc '...' with sudo only when appropriate; good for pipelines/heredocs."""
    base = ["bash", "-lc", cmd_str]
    if need_sudo_prefix():
        base = sudo_prefix_list() + base
    print(f"💻 Running (bash -lc): {cmd_str}")
    rc = subprocess.run(base, env=env or APT_ENV).returncode
    if check and rc != 0:
        print(f"❌ ERROR: Command failed -> {cmd_str}", file=sys.stderr)
        sys.exit(1)
    return rc

# -----------------------------
# cdrom-safe apt update
#   Env knobs:
#     APT_TOUCH_SOURCES=0   -> never modify sources
#     APT_FIX_CDROM=1       -> proactively disable cdrom before update
#     APT_CDROM_MODE=delete -> delete lines instead of comment (default comment)
# -----------------------------
def _cdrom_entries_present() -> bool:
    rc = run_shell(
        r"grep -RHE '^\s*deb\s+cdrom:' /etc/apt/sources.list /etc/apt/sources.list.d/*.list 2>/dev/null",
        check=False
    )
    return rc == 0

def _comment_or_delete_cdrom_entries(mode: str = "comment"):
    print(f"🔧 Disabling CD-ROM repos ({mode}) with backups…")
    if mode not in ("comment", "delete"):
        mode = "comment"
    sed_cmd = r"""sed -i 's/^\s*deb\s\+cdrom:/# deb cdrom:/g'""" if mode == "comment" \
              else r"""sed -i '/^\s*deb\s\+cdrom:/d'"""
    cmd = f"""bash -lc '
      shopt -s nullglob;
      for f in /etc/apt/sources.list /etc/apt/sources.list.d/*.list; do
        [ -f "$f" ] || continue
        if grep -qE "^\s*deb\\s+cdrom:" "$f"; then
          [ -f "$f.bak" ] || cp -a "$f" "$f.bak"
          {sed_cmd} "$f"
        fi
      done
    '"""
    run_shell(cmd, check=False)

def restore_cdrom_sources():
    print("↩️ Restoring any *.bak source lists (if present)…")
    run_shell(
        r"""bash -lc '
          shopt -s nullglob;
          for f in /etc/apt/sources.list /etc/apt/sources.list.d/*.list; do
            [ -f "$f.bak" ] && cp -a "$f.bak" "$f"
          done
        '""",
        check=False
    )

def apt_update_safe():
    """
    Safe `apt update`:
      - No source edits in live sessions (unless forced)
      - Retry after disabling cdrom repos on failure
    """
    touch_sources = os.environ.get("APT_TOUCH_SOURCES", "1") != "0"
    force_fix     = os.environ.get("APT_FIX_CDROM", "0") == "1"
    mode          = (os.environ.get("APT_CDROM_MODE") or "comment").lower()

    # Do not modify sources in live sessions unless explicitly forced
    if is_live() and not force_fix:
        print("🟨 Live session detected: not modifying APT sources.")
        return run(["apt-get", "update", "-y"], check=True)

    # Proactive fix (opt-in)
    if force_fix and touch_sources and _cdrom_entries_present():
        _comment_or_delete_cdrom_entries(mode)

    # First attempt
    rc = run(["apt-get", "update", "-y"], check=False)
    if rc == 0:
        return rc

    # If it failed and cdrom lines exist, try the safe fix and retry
    if touch_sources and _cdrom_entries_present():
        print("⚠️  `apt update` failed and cdrom repos were detected; disabling and retrying…")
        _comment_or_delete_cdrom_entries(mode)
        rc = run(["apt-get", "update", "-y"], check=False)

    if rc != 0:
        sys.exit("❌ `apt update` failed. Check network/proxies or other bad sources.")
    return rc

# -----------------------------
# apt/pip helpers
# -----------------------------
def apt_update():
    # keep simple update helper if you want it elsewhere
    run(["apt-get", "update", "-y"])

def apt_install(packages):
    print("📦 Installing system dependencies (non-interactive)...")
    apt_update_safe()  # <-- use the cdrom-safe version
    base = [
        "apt-get", "install", "-yq",
        "-o", "Dpkg::Options::=--force-confdef",
        "-o", "Dpkg::Options::=--force-confold",
    ]
    run(base + packages)

def pip_install(packages):
    print("🐍 Installing Python packages...")
    run(["python3", "-m", "pip", "install", "--upgrade", "pip", "--break-system-packages"])
    run(["python3", "-m", "pip", "install", "--break-system-packages"] + packages)

# -----------------------------
# OS detection / arch helpers
# -----------------------------
def read_os_release():
    info = {}
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                info[k] = v.strip().strip('"')
    except FileNotFoundError:
        pass
    return info

def is_parrot():
    info = read_os_release()
    id_ = (info.get("ID") or "").lower()
    like = (info.get("ID_LIKE") or "").lower()
    return id_ == "parrot" or "parrot" in like

def dpkg_arch():
    try:
        return subprocess.check_output(["dpkg", "--print-architecture"], text=True).strip()
    except Exception:
        return None

# -----------------------------
# Wireshark / dumpcap (caps → setuid → /usr/local copy)
# -----------------------------
def ensure_group(name):
    if run(["getent", "group", name], check=False) != 0:
        run(["groupadd", "--system", name], check=False)

def add_users_to_group(group, users):
    for u in users:
        if not u:
            continue
        if run(["id", u], check=False) == 0:
            run(["usermod", "-aG", group, u], check=False)

def is_setuid(path):
    try:
        st = os.stat(path)
        return bool(st.st_mode & stat.S_ISUID)
    except FileNotFoundError:
        return False

def getcap(path):
    try:
        return subprocess.check_output(["getcap", path], text=True).strip()
    except Exception:
        return ""

def ensure_dumpcap_nonroot():
    dumpcap = shutil.which("dumpcap")
    if not dumpcap:
        print("ℹ️ dumpcap not found; skipping perms setup.")
        return

    # Prefer capabilities
    run(["setcap", "cap_net_raw,cap_net_admin+eip", dumpcap], check=False)
    caps = getcap(dumpcap)
    if "cap_net_admin,cap_net_raw" in caps and "eip" in caps:
        print(f"✅ dumpcap caps OK: {caps}")
        return

    # Maintainer setuid path
    run_shell("echo 'wireshark-common wireshark-common/install-setuid boolean true' | debconf-set-selections", check=False)
    run(["dpkg-reconfigure", "-f", "noninteractive", "wireshark-common"], check=False)
    if is_setuid(dumpcap):
        print(f"✅ dumpcap setuid OK: {dumpcap}")
        return

    # Final fallback: local copy in /usr/local/bin (first in PATH) with setuid
    local_dump = "/usr/local/bin/dumpcap"
    run(["install", "-o", "root", "-g", "wireshark", "-m", "0750", dumpcap, local_dump], check=False)
    run(["chmod", "u+s", local_dump], check=False)
    # Verify the one we will use
    use_path = shutil.which("dumpcap") or local_dump
    caps2 = getcap(use_path)
    suid2 = is_setuid(use_path)
    print(f"🛠 Using dumpcap at: {use_path}")
    print(f"    caps: {caps2 or 'none'}")
    print(f"    suid: {suid2}")

def preseed_wireshark_and_install():
    """Preseed dumpcap setuid, install wireshark, tshark, caps; add group & users."""
    print("🧪 Preseeding Wireshark (allow non-root capture) and installing non-interactively...")
    run_shell("echo 'wireshark-common wireshark-common/install-setuid boolean true' | debconf-set-selections")
    apt_install(["wireshark", "wireshark-common", "tshark", "libcap2-bin"])
    ensure_group("wireshark")
    target_user = os.environ.get("SUDO_USER") or os.environ.get("USER") or ""
    add_users_to_group("wireshark", [target_user, "user", "parrot"])
    ensure_dumpcap_nonroot()

# -----------------------------
# Steghide installers
# -----------------------------
def install_steghide_deb():
    print("🕵️ Checking Steghide version...")
    try:
        out = subprocess.check_output(["steghide", "--version"], text=True).strip()
        if "0.6.0" in out:
            print("✅ Steghide 0.6.0 already installed.")
            return
    except Exception:
        print("ℹ️ Steghide not found or outdated. Installing patched version...")

    if dpkg_arch() not in ("amd64",):
        print("⚠️ Patched .deb is built for amd64. Falling back to repo install.")
        apt_install(["steghide"])
        return

    apt_install(["wget"])
    print("⬇️ Downloading Steghide 0.6.0 .deb package...")
    run(["wget", "-q", STEGO_DEB_URL, "-O", "/tmp/steghide.deb"])

    print("📦 Installing patched Steghide (auto-fix deps if needed)...")
    rc = run(["dpkg", "-i", "/tmp/steghide.deb"], check=False)
    if rc != 0:
        run([
            "apt-get", "-f", "install", "-yq",
            "-o", "Dpkg::Options::=--force-confdef",
            "-o", "Dpkg::Options::=--force-confold",
        ])
    run(["rm", "-f", "/tmp/steghide.deb"])

    # Only pin on Parrot, where the repo downgrade bug exists
    if is_parrot():
        print("📌 Pinning Steghide 0.6.0 on Parrot to prevent downgrade...")
        pin_contents = """Package: steghide
Pin: version 0.6.0*
Pin-Priority: 1001
"""
        run_shell(f"cat > /tmp/steghide-pin <<'EOF'\n{pin_contents}EOF")
        run(["mv", "/tmp/steghide-pin", "/etc/apt/preferences.d/steghide"])

def install_steghide_auto(mode: str = "auto"):
    """
    mode: 'auto' (default), 'deb', or 'apt'
      - auto: Parrot => deb; Others => apt
      - deb: force patched .deb path (still checks arch)
      - apt: force repo install
    ENV override: FORCE_STEGHIDE_DEB=1 behaves like mode='deb' when mode='auto'
    """
    env_force = os.environ.get("FORCE_STEGHIDE_DEB") == "1"
    if env_force and mode == "auto":
        mode = "deb"

    if mode not in ("auto", "deb", "apt"):
        print(f"⚠️ Unknown steghide mode '{mode}', falling back to 'auto'")
        mode = "auto"

    if mode == "apt" or (mode == "auto" and not is_parrot()):
        print("🧩 Installing Steghide from distro repositories...")
        apt_install(["steghide"])
        return

    print("🧩 Installing Steghide via patched .deb...")
    install_steghide_deb()

# -----------------------------
# Helpers to mirror live-CD UX
# -----------------------------
def ensure_john_and_helpers_on_path():
    print("🧰 Ensuring john/*2john helpers are in PATH...")
    # john symlink
    for cand in ("/usr/sbin/john", "/usr/bin/john"):
        if os.path.exists(cand) and os.access(cand, os.X_OK):
            run(["ln", "-sf", cand, "/usr/local/bin/john"], check=False)
            break
    # /usr/sbin/*2john
    for root in ("/usr/sbin",):
        if os.path.isdir(root):
            for name in os.listdir(root):
                if name.endswith("2john"):
                    src = os.path.join(root, name)
                    if os.access(src, os.X_OK):
                        run(["ln", "-sf", src, f"/usr/local/bin/{name}"], check=False)
    # /usr/share/john/*2john + *2john.py (wrap if not executable)
    share = "/usr/share/john"
    if os.path.isdir(share):
        for name in os.listdir(share):
            if name.endswith("2john") or name.endswith("2john.py"):
                src = os.path.join(share, name)
                dst = f"/usr/local/bin/{name}"
                if os.access(src, os.X_OK):
                    run(["ln", "-sf", src, dst], check=False)
                else:
                    wrapper = f"""#!/usr/bin/env bash
exec python3 "{src}" "$@"
"""
                    run_shell(f"cat <<'EOF' | tee {shlex.quote(dst)} >/dev/null\n{wrapper}EOF")
                    run(["chmod", "+x", dst], check=False)

def install_cyberchef_offline():
    print("🧁 Installing offline CyberChef + desktop entry...")
    apt_install(["curl", "xdg-utils", "desktop-file-utils"])
    CYBER_DIR = "/opt/cyberchef"
    run(["mkdir", "-p", CYBER_DIR])
    index = f"{CYBER_DIR}/index.html"
    if not os.path.exists(index) or os.path.getsize(index) == 0:
        run(["curl", "-fsSL", "https://gchq.github.io/CyberChef/", "-o", index], check=False)
    desktop_entry = """[Desktop Entry]
Type=Application
Name=CyberChef (Offline)
Exec=xdg-open file:///opt/cyberchef/index.html
Icon=utilities-terminal
Terminal=false
Categories=Utility;Education;Development;
"""
    run_shell(f"cat <<'EOF' | tee /usr/share/applications/cyberchef.desktop >/dev/null\n{desktop_entry}EOF")
    run_shell("command -v update-desktop-database >/dev/null && update-desktop-database || true", check=False)

def clone_repo():
    if os.path.exists(REPO_DIR):
        print(f"ℹ️ Repository already exists at {REPO_DIR}")
        return
    print(f"🔁 Cloning the take-home CTF repository into {REPO_DIR} ...")
    apt_install(["git"])
    run(["git", "clone", REPO_URL, REPO_DIR])

# -----------------------------
# CLI
# -----------------------------
def parse_args():
    p = argparse.ArgumentParser(description="CCRI STEM Day Take-Home setup")
    p.add_argument("--steghide-mode",
                   choices=["auto", "deb", "apt"],
                   default="auto",
                   help="Install Steghide using patched deb, repo apt, or auto (default)")
    return p.parse_args()

def main():
    args = parse_args()

    # In live sessions, require root so we never call sudo inside the script.
    if is_live() and not is_root():
        sys.exit("This is a live-CD session. Please run as root (e.g., `sudo -E python3 setup_home_version.py`).")

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
        "binwalk", "fcrackzip", "john", "radare2", "hexedit", "feh", "imagemagick",
        # parity niceties
        "eog", "p7zip-full", "ncat",
    ]
    apt_install(apt_packages)

    # OS-aware Steghide
    install_steghide_auto(args.steghide_mode)

    # Helpers on PATH, offline CyberChef, Ruby zsteg, Python deps
    ensure_john_and_helpers_on_path()
    install_cyberchef_offline()
    install_zsteg()
    pip_install(["flask", "markupsafe"])

    # Clone the take-home repo
    clone_repo()

    print("\n🎉 Setup complete!")
    print(f"📂 Your CTF folder is here: {REPO_DIR}")
    print("▶️ To start the CTF hub:")
    print(f"   cd {REPO_DIR} && python3 start_web_hub.py")
    print("ℹ️ If tshark non-root capture fails, log out/in once to apply wireshark group membership.")

if __name__ == "__main__":
    main()
