import time
import sys
from datetime import datetime
from listener import listen_for_wake_word
from stt.speech_to_text import transcribe
from llm.brain import ask_llm
from tts.speak import speak
from commands.system_commands import open_chrome
from commands.system_commands import open_spotify
from commands.system_commands import play_song


PORCUPINE_ACCESS_KEY = "EM/8PrzGu3j2UUijZq0Jvb6tBspQ8uNIGn8AQXCkEf03ShOn7UgZkg=="
PPN_PATH = "wakeword/jarvis.ppn"

def get_time():
    from datetime import datetime
    return datetime.now().strftime("It is %I:%M %p")


def main():
    while True:
        print("🟢 JARVIS is listening for wake word...")
        listen_for_wake_word(PPN_PATH, PORCUPINE_ACCESS_KEY)

        speak("Hello sir, how can I help you?")
        time.sleep(0.4)

        # Conversation mode
        while True:
            print("🎙️ Listening...")
            user_input = transcribe()

            if not user_input:
                speak("I did not catch that.")
                continue

            text = user_input.lower()

            # 🔴 FULL EXIT
            if any(i in text for i in ["exit", "quit", "shutdown"]):
                speak("Shutting down. Goodbye sir.")
                sys.exit(0)

            # 💤 SLEEP MODE
            if any(i in text for i in ["sleep", "go to sleep", "stop listening"]):
                speak("Going back to sleep.")
                time.sleep(0.5)
                break

            # ⏰ LOCAL TIME (spoken clearly)
            if "time" in text:
                speak(get_time())
                time.sleep(0.4)
                continue
            
            # System commands (REAL actions)
            if "open chrome" in text or "open google chrome" in text:
                speak("Opening Chrome.")
                open_chrome()
                continue

            # OPEN SPOTIFY
            if "open spotify" in text:
                speak("Opening Spotify.")
                open_spotify()
                continue
            
            # PLAY SONG ON SPOTIFY
            if text.startswith("play"):
                song = text.replace("play", "").strip()
                speak(f"Playing {song} on Spotify.")
                success = play_song(song)

                if not success:
                    speak("Sorry, I could not find that song.")
                continue


            # 🧠 AI RESPONSE
            response = ask_llm(user_input)
            speak(response)
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 JARVIS stopped manually.")
