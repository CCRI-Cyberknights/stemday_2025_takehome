# 🎯 CCRI STEM Day CTF – Take-Home Version

Welcome to the **CCRI CyberKnights Capture The Flag Challenge!** 🧠💻  
This is the same environment you experienced during STEM Day, now ready for you to explore at home!

---

## 🚀 Quick Setup (One Step)

Run this in a terminal on **Parrot OS** or any Debian/Ubuntu system:

```bash
curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025_takehome/main/setup_home_version.py | python3 -
````

This will:

* Install all required tools and dependencies
* Download and install the patched Steghide version
* Install `zsteg` for image forensics
* Clone the **take-home CTF repository** to your home folder (`~/stemday2025_takehome`)

---

## ▶️ Launching the Challenge Hub

After setup:

1. Go to your desktop and double-click **`Launch_CCRI_CTF_HUB.desktop`**

   * If it doesn’t open, right-click → **Properties → Permissions** → enable **“Allow this file to run as a program”**

2. Or run manually in a terminal:

   ```bash
   cd ~/stemday2025_takehome
   python3 start_web_hub.py
   ```

   Then open [http://localhost:5000](http://localhost:5000) in your browser.

To stop it:

```bash
python3 stop_web_hub.py
```

---

## 🧭 Guided vs Solo Modes

* **Guided Mode** – Interactive hints and scripts to help solve each challenge
* **Solo Mode** – Same challenges, minimal hints for independent play

Switch between modes from the hub’s top navigation.

---

## 🧩 How to Play

* Each challenge has a **flag** like:

  ```
  CTF{example_flag_here}
  ```
* Enter the flag and click **Submit**:

  * ✅ Correct: green checkmark appears
  * ❌ Incorrect: try again

---

## 🧠 Tips

* Start in **Guided Mode** if you’re new
* Read the `README.txt` in each challenge folder for clues
* Try different tools — each challenge teaches something new

---

Have fun and good luck! 🎉