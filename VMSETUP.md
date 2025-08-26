# 🧠 CCRI CyberKnights STEM Day – Take-Home CTF Guide

Welcome! 🎉  
This USB has a **Parrot OS Take-Home VM** so you can keep exploring the Capture The Flag (CTF) challenges on your own computer.

---

## 🔧 Requirements
- Computer with at least:
  - 2 CPU cores free
  - 4 GB of RAM free
  - ~30 GB free disk space
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

---

## 🚀 Setup Steps

### 1. Install VirtualBox
- Use the installer on this USB (`VirtualBox-Installer.exe` for Windows, `.dmg` for macOS)  
- Or download from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)

### 2. Create a New VM
- **Name:** ParrotOS-STEMDay  
- **Type:** Linux  
- **Version:** Debian (64-bit)  
- **Memory:** 4096 MB (4 GB)  
- **CPUs:** 2 cores  
- **Disk:** VDI, Dynamically allocated, 30 GB  

### 3. Attach the ISO
- Settings → Storage → Empty CD icon → **Choose a disk file**  
- Select `Parrot-STEMDay.iso` from this USB  

---

## 💿 Installing Parrot OS (from Live-CD)

1. Start the VM  
2. At the boot menu choose **Try/Install Parrot OS**  
   - This loads the **Live desktop**  
3. On the desktop, double-click **Install Parrot**  
4. Follow the installer:  
   - Language: English  
   - Location: defaults  
   - Keyboard: US  
   - User setup:  
     - Full name: `parrot`  
     - Username: `parrot`  
     - Password: `parrot`  
     - Computer name: `parrot`  
   - Partitioning: **Erase disk and install Parrot**  
   - Confirm and continue  
5. Wait ~10–15 minutes  
6. Restart → press **Enter** if asked to remove media  

---

## 👤 Login
- Username: `parrot`  
- Password: `parrot`  

---

## 🎮 Launch the CTF
1. Log in after reboot  
2. On the desktop, double-click **CCRI STEM Day CTF**  
3. The CTF hub opens in your browser 🎉  

---

## 🆘 Tips
- If the VM is slow, assign at least **2 cores + 4 GB RAM**  
- If things break, delete the VM and reinstall from the ISO  
- Reinstalling only affects the VM, not your real computer  
