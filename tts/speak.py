import subprocess
import os
import sounddevice as sd
import soundfile as sf

PIPER_PATH = r"D:\JARVIS\piper\piper.exe"
MODEL_PATH = r"D:\JARVIS\piper\models\en_US-lessac-medium.onnx"
AUDIO_FILE = "response.wav"

def speak(text):
    print(f"🔊 JARVIS: {text}")

    # Generate speech using Piper
    process = subprocess.Popen(
        [PIPER_PATH, "-m", MODEL_PATH, "-f", AUDIO_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True
    )
    process.stdin.write(text)
    process.stdin.close()
    process.wait()

    # 🔊 Play audio synchronously (BLOCKING)
    data, samplerate = sf.read(AUDIO_FILE)
    sd.play(data, samplerate)
    sd.wait()   # ⬅️ IMPORTANT: wait until finished
