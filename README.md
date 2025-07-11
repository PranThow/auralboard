<<<<<<< HEAD
# 🔊 Auralboard

A lightweight, open-source Python soundboard that plays MP3s via VB-Cable and supports real-time microphone passthrough.

## 📦 Download

👉 [Download Auralboard v0.1a](https://github.com/PranThow/auralboard/releases/latest)  
No Python required — just double-click and go!

## 🚀 Features
- Dynamic grid of MP3 buttons
- Audio routed through VB-Cable
- Hear-your-own-sound toggle
- Mic passthrough to VB-Cable output
- Saves and loads layouts (save.json)

## ⚠️ Known Issues

- ❗ GUI can lag or freeze with large soundboards
- ❗ Some systems may have audio glitches during heavy playback
- ❗ No visual confirmation when a sound finishes
- ❗ Code is messy (first alpha) — expect bugs!
- ❗ A ~0.5 second delay when playing a sound
- ❗ A ~2.5 second delay when hearing a sound
-  And much more!

## 🛣️ Roadmap

- ✅ Add VB-Cable compatibility
- ✅ GUI-based grid system
- ✅ `.exe` build for non-coders
- ❌ Keybinds
- ❌ Drag-and-drop sound support
- ❌ Visual feedback when sound plays
- ❌ Auto-install VB-Cable
- ❌ Looping / stop buttons
- ❌ Volume control per sound
- ❌ Themes or skinning
- ❌ Total rewrite in C++ or Rust

💬 Got a feature idea? Submit an issue!

## 📃 Requirements
- Python 3.9 or newer
- VB-Cable (Install from [vb-audio.com/Cable](https://vb-audio.com/Cable/))
- Dependencies in `requirements.txt`

## 🔊 VB-Cable Required (But Don't Worry!)

This app uses **VB-Cable** to route sound to virtual outputs. It’s free but must be installed manually (for now).

> 🛠️ **Auto-install coming soon!**  
> The app will eventually install VB-Cable for you — no tech skills needed.

### 🔗 Install Instructions:
1. Go to [vb-audio.com/Cable](https://vb-audio.com/Cable/)
2. Download and extract the ZIP
3. Run `VBCABLE_Setup_x64.exe` **as Administrator**
4. Click “Install Driver”
5. Reboot your computer

⚠️ If VB-Cable isn’t installed, the app won’t be able to play or route audio!

## 🧰 FFmpeg
This app includes a bundled copy of FFmpeg in `ffmpeg/bin/ffmpeg.exe` for audio decoding.

FFmpeg is licensed under the [LGPL/GPL license](https://ffmpeg.org/legal.html).

## 🔧 Installation

```bash
pip install -r requirements.txt
python main.py
```

## 📄 License

Licensed under the **GNU GPLv3** — see [LICENSE](LICENSE) for details.  
