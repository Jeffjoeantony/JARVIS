import pvporcupine
import pyaudio
import struct

def listen_for_wake_word(ppn_path, access_key):
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[ppn_path]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🟢 JARVIS is listening for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)
            if result >= 0:
                print("🔔 Wake word detected!")
                return
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
