import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import scipy.io.wavfile as wav

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def record_audio(duration=5, fs=16000):
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write("input.wav", fs, audio)
    return "input.wav"

def transcribe():
    audio_file = record_audio()
    segments, _ = model.transcribe(audio_file)
    text = ""
    for segment in segments:
        text += segment.text
    print("📝 You said:", text)
    return text.strip()
