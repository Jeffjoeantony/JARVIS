import subprocess
import os
import platform
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "a665d39ccf2b4ca0b8c0dfed0475a892"
SPOTIPY_CLIENT_SECRET = "a5f87b197a3c41f29915c807897017ae"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

scope = "user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope
    )
)

def open_chrome():
    system = platform.system()

    if system == "Windows":
        # Most reliable Windows Chrome launch
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path):
            subprocess.Popen([chrome_path])
            return True
        else:
            # fallback
            subprocess.Popen(["start", "chrome"], shell=True)
            return True

    return False

def open_spotify():
    system = platform.system()
    
    if system == "Windows":
        try:
            subprocess.Popen(
                "start spotify:",
                shell=True
            )
            return True
        except:
            pass
    
    return False

def play_song(song_name):
    # 🔹 GET ACTIVE DEVICES
    devices = sp.devices()
    print(devices) 

    if not devices['devices']:
        print("No active Spotify device found")
        return

    device_id = devices['devices'][0]['id']

    results = sp.search(q=song_name, type='track', limit=1)
    track_uri = results['tracks']['items'][0]['uri']

    # 🔹 PLAY SONG ON DESKTOP APP
    sp.start_playback(device_id=device_id, uris=[track_uri])