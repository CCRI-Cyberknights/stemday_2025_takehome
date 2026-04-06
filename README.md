Due to the rolling update nature of Parrot OS, since they are on 7.1 as of writing and this is a 6.4 project, downloading proper dependancies is a bit broken, as the newest downloads expect the latest version of things. Therefore I am archiving this as supporting such a version change is out of scope of this project.

# 🎯 CCRI STEM Day CTF – Take-Home Version

Welcome to the **CCRI CyberKnights Capture The Flag Challenge!** 🧠💻
This is the same environment you experienced during STEM Day, now ready for you to explore at home!

---

## 🚀 Quick Setup (Three Steps)

1.  **Get the OS:**
    Download **Parrot OS** from here (either *Home* or *Security* edition):
    👉 [https://www.parrotsec.org/download/](https://www.parrotsec.org/download/)

    > ⚠️ *Other Linux distros (like Linux Mint) should work, but Parrot OS is the tested environment.*

2.  **Configure the VM:**
    Follow our setup guide here: [VMSETUP.md](https://github.com/CCRI-Cyberknights/stemday_2025_takehome/blob/main/VMSETUP.md)

3.  **Install the Challenge:**
    Open a terminal in your new VM and run this command:

    ```bash
    curl -fsSL 'https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025_takehome/main/setup_home_version.py' | python3 -
    ```

    **This script will:**
    * Install required tools (Python/Flask dependencies).
    * Install forensic tools (`steghide`, `zsteg`).
    * Clone the challenge repository to: `~/Desktop/stemday_2025_takehome`

---

## 🗂️ Project Layout

Once installed, your folder will look like this:

```text
stemday_2025_takehome/
├── challenges/                 # Exploration Mode (Guided scripts)
├── challenges_solo/            # Solo Mode (Hard mode)
├── web_version/                # The Web Portal source code
├── coach_core.py               # Coach Mode Engine
├── exploration_core.py         # Exploration Engine
├── worker_node.py              # Background Task Manager
├── start_web_hub.py            # Launcher Script
├── stop_web_hub.py             # Shutdown Script
├── reset_environment.py        # 🧹 Cleanup Tool
├── ccri_ctf.pyz                # 🔒 Core Logic Bundle
└── Launch_CCRI_CTF_HUB.desktop # Desktop Shortcut
```

---

## ▶️ Launching the Challenge Hub

1.  Open the folder `~/Desktop/stemday_2025_takehome`.
2.  **Move the file `Launch_CCRI_CTF_HUB.desktop` out of the folder and onto your Desktop.**
3.  Double-click the icon to start.
    * *Note: If it doesn’t open, right-click → **Properties → Permissions** → check **“Allow this file to run as a program”**.*

### Manual Launch (Alternative)
If the shortcut fails, you can run it from the terminal:

```bash
cd ~/Desktop/stemday_2025_takehome
./start_web_hub.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

To stop the hub:
```bash
./stop_web_hub.py
```

---

## 📜 Script Reference

You will see several Python scripts in the folder. Here is what they do:

| Script | Purpose |
| :--- | :--- |
| **`start_web_hub.py`** | Starts the web server where you submit flags. |
| **`reset_environment.py`** | **Fix-It Tool.** Run this to delete all generated files and reset challenges to their original state. Useful if you accidentally delete a flag! |
| **`coach_core.py`** | The engine powering **Coach Mode** (see below). |
| **`ccri_ctf.pyz`** | The "Game Cartridge". Contains the validation logic for flags. **Do not delete.** |

---

## 🧭 Modes of Play

* **Exploration Mode** (Recommended for Beginners):
    In this track, each challenge folder contains two different scripts. You generally run one or the other using the **buttons on the Web Hub**:
    * **Exploration Mode** (via the helper/solver script) is a high-level demo of what a CTF is. It performs the actual work behind the scenes—running real commands on real files—to show you the result immediately.
    * **Coach Mode** is an interactive, command-by-command guide that walks you through the steps to solve the puzzle yourself.

* **Solo Mode** (Hard Mode):
    Inside `challenges_solo/`, you get the same puzzles but **no scripts and no coach**. You must rely entirely on your own Linux knowledge and tools to find the flags.

---

## 🧩 How to Play

1.  **Find the Flag:**
    Each challenge hides a flag text string. It always follows this format:
    ```text
    CCRI-AAAA-1111
    ```
2.  **Submit:**
    Enter the flag into the web hub and click **Submit**.
    * ✅ **Correct:** You get points and the challenge is marked complete.
    * ❌ **Incorrect:** Check your spelling and try again!

---

## 🧠 Tips

* **New to Linux?** Start in **Exploration Mode** and use the **Launch Coach Mode** button!
* **Stuck?** Read the `README.md` inside each challenge folder for specific clues.
* **Broken Challenge?** Run `./reset_environment.py` to wipe the slate clean of generated files and try again. If you accidentially removed something critical, redownload the challenge from github again.

Have fun and good luck! 🎉
