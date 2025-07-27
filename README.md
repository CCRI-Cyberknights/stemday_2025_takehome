# 🎯 CCRI STEM Day CTF – Take-Home Version

Welcome to the **CCRI CyberKnights Capture The Flag Challenge!** 🧠💻  
This folder contains the full CTF environment we handed out during STEM Day. It works offline, directly from your VM or installed Parrot OS system.

---

## 🚀 Getting Started

### ▶️ Step 1: Launch the Challenge Hub

Double-click the **`Launch_CCRI_CTF_HUB.desktop`** icon on your desktop.  
If it doesn't open right away:

1. Right-click the file → **Properties**
2. Go to the **Permissions** tab
3. ✅ Check “Allow this file to run as a program”

This will launch the CTF hub in your browser where you can pick a challenge.

---

### 🧭 Guided vs Solo Mode

You can choose between two ways to play:

- **Guided Mode** – beginner-friendly, includes interactive hints and scripts to walk you through each step
- **Solo Mode** – same challenges, but no helper scripts or guidance — just you and your skills!

You can switch between these in the top navigation of the CTF hub.

---

## 🧩 Solving Challenges

Each challenge will ask you to find a **flag** — a string that looks like this:

```
CTF{example_flag_here}
```

Once you think you’ve found it, enter it into the challenge’s text box and click **Submit**.

- ✅ Correct: The challenge button will show a green checkmark
- ❌ Incorrect: You’ll be told it’s wrong so you can try again

Some flags might require you to:
- Decode text
- Crack a password
- Analyze a file
- Scan a fake network

Each challenge is different!

---

## 🧠 Tips for Success

- Use the **Guided Mode** if you're new — it’s designed to teach you.
- If something doesn’t seem to work, try reading the challenge folder’s `README.txt` or run its `.sh` script.
- The challenges are meant to be tricky — don’t be afraid to experiment!

---

## 💡 Want to Run the Hub Manually?

If you ever want to launch the challenge hub yourself from the terminal:

```bash
cd ~/Desktop/stemday_2025_takehome
python3 start_web_hub.py
```

Then open your browser and go to:  
[http://localhost:5000](http://localhost:5000)

To stop it:

```bash
python3 stop_web_hub.py
```

---

## ❓ Need Help?

Ask your instructor or a CCRI CyberKnights club member — we’d be happy to help.

Or feel free to explore the folders and learn by tinkering!

---

## 🧡 Good Luck and Have Fun!

We hope you enjoy solving these puzzles and exploring the world of cybersecurity.  
— The **CCRI CyberKnights**
