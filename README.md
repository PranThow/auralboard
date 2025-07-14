# 🔊 Auralboard

🎙️ A lightweight, open-source soundboard built in Python.  
Plays MP3s via VB-Cable and supports real-time mic passthrough.

## ‼️ VERSION 0.2-ALPHA IS FINALLY HERE

Version 0.2-Alpha is finally here! This major update includes

- ⚡ Significantly decreased delay when playing a sound
- 🟢 Visual feedback when a sound is playing
- 🛑 A stop button when playing a sound
- 🧠 A partial C++ rewrite for some things
- 🖱️ An ability to change the audio file in a button by right clicking
- 🧱 A fixed `.exe` build for the app

## 📦 Download

👉 [Download Auralboard v0.2-alpha for Windows 8.1+ x64](https://github.com/PranThow/auralboard/releases/download/v0.2-alpha/auralboard-win-v0.2-alpha.exe)  

## 🖥️ High-DPI Display Flix (Blurry Text on 4K)

If the app looks blrury or fuzzy on a high-resolution monitor (like 4K), it's due to Windows scaling

### 🔧 Fix:

1. Right-click the `.exe` or `main.py`
2. Click Properties > Compatibility
3. Click `Change high DPI settings`
4. Check `Override high DPI scaling behavior`
5. Set scaling performed by: `Application`

## 🚀 Features

- Dynamic grid of MP3 buttons
- Audio routed through VB-Cable
- “Hear your own soundboard” toggle
- Mic passthrough to VB-Cable
- Saves/loads grid layout from `save.json`

## ⚠️ Known Issues

### 🖱️ GUI

- ❗ UI may lag with many buttons
- ❗ Blurry text when used on a 4K monitor due to Windows scaling

## 🛣️ Roadmap

- ✅ VB-Cable support
- ✅ Grid GUI layout
- ✅ Standalone `.exe` build
- ✅ Layout saving/loading
- ✅ Visual feedback on play/pause
- ✅ Stop buttons 
- 🔜 Full C++ rewrite
- 🔜 Auto-install VB-Cable
- 🔜 Drag-and-drop support
- 🔜 Looping + per-button volume
- 🔜 Custom skins/themes
- 🔜 Keybinds

💡 Got an idea? [Submit an issue!](https://github.com/PranThow/auralboard/issues)

## 📃 Requirements (Python Version Only)

- Python 3.9+
- VB-Cable ([Download here](https://vb-audio.com/Cable/))
- FFmpeg (included in `/ffmpeg/` folder)
- Dependencies listed in `requirements.txt`

## 🔊 VB-Cable Setup

This app **requires VB-Cable** to route sound to virtual outputs.  
It’s free and takes 2 minutes to install:

1. Go to [vb-audio.com/Cable](https://vb-audio.com/Cable/)
2. Download and extract the ZIP
3. Run `VBCABLE_Setup_x64.exe` as **Administrator**
4. Click “Install Driver”
5. **Reboot your computer**

> 🛠️ Auto-installation coming soon!

## 🧰 FFmpeg

Auralboard uses FFmpeg to decode MP3s.  
FFmpeg is licensed under [LGPL/GPL](https://ffmpeg.org/legal.html).

## 🔧 Installation (Python version)

```bash
pip install -r requirements.txt
python main.py
```