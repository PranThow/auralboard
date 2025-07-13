# 🔊 Auralboard

🎙️ A lightweight, open-source soundboard built in Python.  
Plays MP3s via VB-Cable and supports real-time mic passthrough.

## ⚠️ Notice — FFmpeg Not Bundled in `.exe` Yet!

**The current `.exe` build does _not_ include FFmpeg.**  
Please use the **Python version** until the next release. Thank you!

## 📦 Download

👉 [Download Auralboard v0.1-alpha](https://github.com/PranThow/auralboard/releases/latest)  
_No Python required – just double-click and go!_  
⚠️ *MP3 playback requires FFmpeg (Python version only for now).*

## 🚀 Features

- Dynamic grid of MP3 buttons
- Audio routed through VB-Cable
- “Hear your own soundboard” toggle
- Mic passthrough to VB-Cable
- Saves/loads grid layout from `save.json`

## ⚠️ Known Issues

### 🎵 Audio / Playback

- ❗ ~0.5s delay when playing a sound *(fixed in next release!)*
- ❗ ~2.5s delay when monitoring via “hear” *(fixed in next release!)*
- ❗ No visual feedback when sound ends *(fixed in next release!)*
- ❗ Occasional audio glitches if spamming buttons

### 🖱️ GUI

- ❗ UI may lag with many buttons
- ❗ Buttons don’t show “playing” state yet *(next release!)*
- ❗ No drag-and-drop or keybinds *(planned)*

## 🛣️ Roadmap

- ✅ VB-Cable support
- ✅ Grid GUI layout
- ✅ Standalone `.exe` build
- ✅ Layout saving/loading
- 🔜 Visual feedback on play/pause *(next release for pause only)*
- 🔜 Full C++ rewrite *(partial in next release)*
- 🔜 Stop buttons *(next release!)*
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

> 🛠️ Auto-installation coming in future updates!

## 🧰 FFmpeg (Python Version Only)

Auralboard uses FFmpeg to decode MP3s.  
FFmpeg is licensed under [LGPL/GPL](https://ffmpeg.org/legal.html).

> ⚠️ The `.exe` version **does not bundle FFmpeg** yet — only the Python version supports MP3 playback currently.

## 🔧 Installation (Python version)

```bash
pip install -r requirements.txt
python main.py
