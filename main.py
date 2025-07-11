import tkinter as tk
import sounddevice as sd
import threading
import os
import json
import tempfile
import simpleaudio as sa
from pydub import AudioSegment
from tkinter import ttk, messagebox, filedialog
from pushaudio import play

# ---------------- Global Variables ---------------- #
stream = None
button_file_map = {}
temp_dir = os.path.join(tempfile.gettempdir(), "auralboard_wavcache")
os.makedirs(temp_dir, exist_ok=True)

# ---------------- Wav Conversion ---------------- #
def convert_to_wav(mp3_path):
    base = os.path.basename(mp3_path)
    wav_filename = os.path.splitext(base)[0] + ".wav"
    wav_path = os.path.join(temp_dir, wav_filename)

    try:
        sound = AudioSegment.from_file(mp3_path)
        sound.export(wav_path, format="wav")
    except Exception as e:
        print(f"MP3 to WAV conversion failed: {e}")
        return None

    return wav_path

# ---------------- Saveing & Loading ---------------- #
def save_button_map():
    data = {}
    for widget in button_frame.winfo_children():
        info = widget.grid_info()
        key = f"{info['row']},{info['column']}"
        entry = button_file_map.get(widget)
        data[key] = entry if entry else None

    try:
        with open("save.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving layout: {e}")

def load_button_map():
    for i in range(100):
        button_frame.grid_rowconfigure(i, weight=0)
        button_frame.grid_columnconfigure(i, weight=0)

    if not os.path.exists("save.json"):
        return

    try:
        with open("save.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading layout: {e}")
        return

    for widget in button_frame.winfo_children():
        widget.destroy()
    button_file_map.clear()

    positions = [tuple(map(int, k.split(','))) for k in data.keys()]
    if not positions:
        return

    max_row = max(r for r, _ in positions) + 1
    max_col = max(c for _, c in positions) + 1

    for row in range(max_row):
        for col in range(max_col):
            key = f"{row},{col}"
            btn = ttk.Button(button_frame)
            btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10, sticky="nsew")

            entry = data.get(key)
            if entry and isinstance(entry, dict):
                btn.config(text=os.path.basename(entry["mp3"]))
                btn.config(command=lambda b=btn: play_mp3(b))
                button_file_map[btn] = entry
            else:
                btn.config(text="Pick MP3", command=lambda b=btn: pick_mp3_file(b))

    for r in range(max_row):
        button_frame.grid_rowconfigure(r, weight=1)
    for c in range(max_col):
        button_frame.grid_columnconfigure(c, weight=1)

    width_var.set(str(max_col))
    height_var.set(str(max_row))

# ---------------- Microphone Handling ---------------- #
def get_filtered_mics():
    devices = sd.query_devices()
    mics = []
    seen_names = set()

    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            name = dev['name']
            if any(x in name for x in [
                "Mapper", "Primary", "(@System32", "Wave", "Hands-Free", "HF Audio",
                "VAC (W)", "Steam", "VB-Audio", "Point", "Realtek", "NVIDIA", "Output", "()"
            ]) or name.strip() == "":
                continue

            clean_name = name.strip()
            if clean_name not in seen_names:
                seen_names.add(clean_name)
                mics.append((i, name))
    return mics

def find_device_by_name(partial_name, is_input=True):
    partial = partial_name.lower().strip()
    for i, dev in enumerate(sd.query_devices()):
        name = dev['name'].lower()
        if partial in name:
            if is_input and dev['max_input_channels'] > 0:
                return i
            if not is_input and dev['max_output_channels'] > 0:
                return i
    return None

# ---------------- Passthrough ---------------- #
def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(f"Stream warning: {status}")
    outdata[:] = indata

def start_passthrough(mic_name):
    global stream
    stop_passthrough()

    mic_id = find_device_by_name(mic_name, is_input=True)
    vb_id = find_device_by_name("CABLE Input", is_input=False)

    if mic_id is None:
        messagebox.showerror("Error", f"Microphone '{mic_name}' not found.")
        return
    if vb_id is None:
        messagebox.showerror("Error", "'CABLE Input' output device not found.")
        return

    try:
        stream = sd.Stream(device=(mic_id, vb_id),
                           samplerate=44100,
                           blocksize=1024,
                           channels=1,
                           dtype='float32',
                           callback=audio_callback)
        stream.start()
        print(f"Passthrough started: {mic_name} → CABLE Input")
    except Exception as e:
        messagebox.showerror("Passthrough Error", str(e))

def stop_passthrough():
    global stream
    if stream:
        try:
            stream.stop()
            stream.close()
            print("Passthrough stopped.")
        except Exception as e:
            print(f"Error stopping stream: {e}")
        stream = None

def on_mic_selected(event=None):
    mic_name = mic_combo.get()
    if not mic_name:
        return
    threading.Thread(target=lambda: start_passthrough(mic_name), daemon=True).start()

# ---------------- MP3 Playback ---------------- #
def play_mp3(btn):
    entry = button_file_map.get(btn)
    if entry:
        def do_play():
            # Always play to VB-Cable
            try:
                play(entry["wav"])  # your existing VB-Cable function
            except Exception as e:
                print(f"VB-Cable playback error: {e}")

            # If toggle is ON, also play locally
            if hear_soundboard_var.get():
                try:
                    wave = sa.WaveObject.from_wave_file(entry["wav"])
                    wave.play()
                except Exception as e:
                    print(f"Local playback error: {e}")
        threading.Thread(target=do_play, daemon=True).start()
    else:
        messagebox.showwarning("No File", "Please select an MP3 file first.")



# ---------------- MP3 Button Grid ---------------- #
def pick_mp3_file(btn):
    mp3_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if mp3_path:
        wav_path = convert_to_wav(mp3_path)
        if not wav_path:
            messagebox.showerror("Error", "Failed to convert MP3 to WAV.")
            return

        button_file_map[btn] = {
            "mp3": mp3_path,
            "wav": wav_path
        }
        btn.config(text=os.path.basename(mp3_path))
        btn.config(command=lambda b=btn: play_mp3(b))
        save_button_map()

def create_grid():
    try:
        rows = int(height_var.get())
        cols = int(width_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Width and height must be integers.")
        return

    old_buttons = {}
    for btn, entry in button_file_map.items():
        info = btn.grid_info()
        key = (info['row'], info['column'])
        old_buttons[key] = entry

    for widget in button_frame.winfo_children():
        widget.destroy()
    button_file_map.clear()

    for i in range(100):
        button_frame.grid_rowconfigure(i, weight=0)
        button_frame.grid_columnconfigure(i, weight=0)

    for r in range(rows):
        for c in range(cols):
            key = (r, c)
            btn = ttk.Button(button_frame)
            btn.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=10, sticky="nsew")

            if key in old_buttons:
                entry = old_buttons[key]
                btn.config(text=os.path.basename(entry["mp3"]))
                btn.config(command=lambda b=btn: play_mp3(b))
                button_file_map[btn] = entry
            else:
                btn.config(text="Pick MP3", command=lambda b=btn: pick_mp3_file(b))

    for r in range(rows):
        button_frame.grid_rowconfigure(r, weight=1)
    for c in range(cols):
        button_frame.grid_columnconfigure(c, weight=1)

    save_button_map()

# ---------------- GUI Setup ---------------- #
root = tk.Tk()
root.title("Auralboard")
root.geometry("700x500")
root.minsize(350, 400)
root.protocol("WM_DELETE_WINDOW", lambda: (stop_passthrough(), root.destroy()))

hear_soundboard_var = tk.BooleanVar(value=True)

mics = get_filtered_mics()

ttk.Label(root, text="Select Microphone:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

mic_combo = ttk.Combobox(root, state="readonly", width=40)
mic_combo['values'] = [name for idx, name in mics]
mic_combo.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky="ew")
mic_combo.bind("<<ComboboxSelected>>", on_mic_selected)

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

width_var = tk.StringVar(value="3")
width_frame = ttk.Frame(root)
ttk.Label(width_frame, text="Grid Width:").pack(side="left")
ttk.Entry(width_frame, textvariable=width_var, width=5).pack(side="left")
width_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

ttk.Label(root, text="Grid Height:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
height_var = tk.StringVar(value="2")
height_frame = ttk.Frame(root)
ttk.Label(height_frame, text="Grid Height:").pack(side="left")
ttk.Entry(height_frame, textvariable=height_var, width=5).pack(side="left")
height_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="w")

ttk.Button(root, text="Create Grid", command=create_grid).grid(row=1, column=4, padx=5, pady=5)

ttk.Checkbutton(root, text="Hear Soundboard", variable=hear_soundboard_var).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
root.grid_rowconfigure(4, weight=0)

button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(1, weight=1)

if mics:
    mic_combo.current(0)
    on_mic_selected()

load_button_map()
root.mainloop()
