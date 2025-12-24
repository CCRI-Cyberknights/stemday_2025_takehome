# 🎯 CCRI STEM Day CTF – Take-Home Version

Welcome to the **CCRI CyberKnights Capture The Flag Challenge!** 🧠💻  
This is the same environment you experienced during STEM Day, now ready for you to explore at home!

---

## 🚀 Quick Setup (Three Steps)

Download **Parrot OS** from here, either *Home* for the look or *Security* for the full suite of tools:  
👉 https://www.parrotsec.org/download/

⚠️ Other Linux distros (like Linux Mint) should work, but Parrot OS is the tested environment. The desktop icon may only work in Parrot OS right now.

Follow the instructions here [VMSETUP.md](https://github.com/CCRI-Cyberknights/stemday_2025_takehome/blob/main/VMSETUP.md) to setup the **Parrot OS** iso within **Virtualbox**.

In a terminal on **Parrot OS**, run:

```bash
curl -fsSL [https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025_takehome/main/setup_home_version.py](https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025_takehome/main/setup_home_version.py) | python3 -
```

This will:
* Install all required tools and dependencies
* Download and install the patched Steghide version
* Install `zsteg` for image forensics
* Clone the **take-home CTF repository** to your Desktop at:
  ```
  ~/Desktop/stemday_2025_takehome
  ```

---

## ▶️ Launching the Challenge Hub

After setup:

1. Open the folder `~/Desktop/stemday_2025_takehome`
2. **Move the file `Launch_CCRI_CTF_HUB.desktop` out of the folder and onto your Desktop**
   * This is your shortcut to the challenge hub
3. Double-click **`Launch_CCRI_CTF_HUB.desktop`**
   * If it doesn’t open, right-click → **Properties → Permissions** → enable **“Allow this file to run as a program”**

### Manual launch (alternative)
```bash
cd ~/Desktop/stemday_2025_takehome
python3 start_web_hub.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

To stop the hub:
```bash
python3 stop_web_hub.py
```

---

## 🧭 Exploration vs Solo Modes

* **Exploration Mode** – Interactive hints and scripts to help solve each challenge. This is the recommended "Guided" experience for learning.
* **Solo Mode** – Same challenges and flags, but with minimal hints for independent play.

Switch between modes from the hub’s top navigation.

---

## 🧩 How to Play

* Each challenge contains a hidden **flag** following this format:
  ```
  CCRI-AAAA-1111
  ```
* Enter the flag you find into the hub and click **Submit**:
  * ✅ Correct: A green checkmark appears and the challenge is unlocked.
  * ❌ Incorrect: The flag is rejected; try a different approach!

---

## 🧠 Tips

* Start in **Exploration Mode** if you are new to CTFs or Linux.
* Read the `README.md` in each challenge folder for specific clues and tool suggestions.
* Experiment with the command line — each challenge is designed to teach a new skill.

---

Have fun and good luck! 🎉