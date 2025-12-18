import subprocess
import sounddevice as sd
import soundfile as sf
import threading
import keyboard
import os
import time

PIPER_PATH = r"D:\JARVIS\piper\piper.exe"
MODEL_PATH = r"D:\JARVIS\piper\models\en_US-lessac-medium.onnx"
AUDIO_FILE = "response.wav"

# Shared flag
stop_speaking = False

def _play_audio_interruptible():
    global stop_speaking

    data, samplerate = sf.read(AUDIO_FILE)
    sd.play(data, samplerate)

    while sd.get_stream().active:
        if keyboard.is_pressed("ctrl"):
            stop_speaking = True
            sd.stop()
            break
        time.sleep(0.05)

    sd.stop()

def speak(text):
    global stop_speaking
    stop_speaking = False

    print(f"🔊 JARVIS: {text}")

    # Generate speech
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

    # Play audio in interruptible thread
    t = threading.Thread(target=_play_audio_interruptible)
    t.start()
    t.join()
