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
from commands.location import get_location
from commands.weather import get_weather
from tts.speak import speak, stop_speaking
from rapidfuzz import fuzz

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

            def is_spotify_command(text):
                return fuzz.partial_ratio(text, "spotify") > 70

            if is_spotify_command(text):
                speak("Opening Spotify.")
                open_spotify()
                continue
            
            # PLAY SONG ON SPOTIFY
            if text.startswith("play"):
                song = text.replace("play", "").strip()
            
                open_spotify()  # 🔴 REQUIRED
                speak(f"Playing {song} on Spotify.")
            
                success = play_song(song)
            
                if not success:
                    speak("Sorry, I could not find that song.")
                continue
            
            
            if "location" in text or "where am i" in text:
                speak(get_location())
                continue
            
            if "weather" in text:
                city, region, country = None, None, None

                # get location
                location_text = get_location()

                # extract city from location text
                city = location_text.split("in ")[1].split(",")[0]

                weather = get_weather(city)

                if weather:
                    speak(f"In {city}, {weather}")
                else:
                    speak("Sorry, I could not fetch the weather right now.")

                continue

            
            brief_keywords = [
                "brief me about",
                "brief about",
                "in short",
                "short explanation",
                "what do you know about",
                "tell me briefly"
            ]

            is_brief = any(kw in text for kw in brief_keywords)

            # 🧠 AI RESPONSE
            # response = ask_llm(user_input)
            # speak(response)
            if is_brief:
                response = ask_llm(user_input, mode="brief")
            else:
                response = ask_llm(user_input)

            speak(response)

            # If user interrupted speech, immediately listen again
            if stop_speaking:
                print("🔁 Speech interrupted by user")
                continue


            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 JARVIS stopped manually.")