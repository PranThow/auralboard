import sys
import os
import sounddevice as sd
from pydub import AudioSegment
import numpy as np

# Configure ffmpeg
def configure_ffmpeg():
    if AudioSegment.converter:
        return # already configured
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_exe = "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg"
    ffmpeg_path = os.path.join(base_dir, "ffmpeg", "bin", ffmpeg_exe)

    if os.path.exists(ffmpeg_path):
        AudioSegment.converter = ffmpeg_path
    else:
        raise FileNotFoundError(f"ffmpeg executable not found at {ffmpeg_path}.")

# Make sure that VB-Cable is installed and set up correctly
def find_output_device(name_match="CABLE Input"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if name_match.lower() in dev['name'].lower() and dev['max_output_channels'] > 0:
            return i
    return None

def load_audio(file_path, sample_rate=48000):
    audio = AudioSegment.from_file(file_path).set_frame_rate(sample_rate)

    # Get channels
    num_channels = audio.channels
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    # Normalize
    samples /= float(1 << (8 * audio.sample_width - 1))

    # Reshape based on number of channels
    if num_channels > 1:
        samples = samples.reshape((-1, num_channels))
    else:
        samples = samples.reshape((-1, 1))

    return samples


# Play the audio file through VB-Cable
def play(file_path, device_name="CABLE Input", sample_rate=48000):
    configure_ffmpeg()

    device_id = find_output_device(device_name)
    if device_id is None:
        raise RuntimeError(f"Output device '{device_name}' not found.")
    
    samples = load_audio(file_path, sample_rate)
    
    try:
        sd.play(samples, samplerate=sample_rate, device=device_id, blocking=True)
    except Exception as e:
        raise RuntimeError(f"Failed to play audio: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pushaudio.py <file_path>")
        sys.exit(1)

    try:
        play(sys.argv[1])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)