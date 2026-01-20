import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import time

SPOTIPY_CLIENT_ID = "a665d39ccf2b4ca0b8c0dfed0475a892"
SPOTIPY_CLIENT_SECRET = "a5f87b197a3c41f29915c807897017ae"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

scope = "user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        open_browser=True
    )
)

# 🔹 Open Spotify Desktop App
def open_spotify():
    try:
        subprocess.Popen("spotify:", shell=True)
        time.sleep(5)  # Allow Spotify to register as active device
        return True
    except:
        return False

# 🔹 Play song on Desktop App (NOT Web)
def play_song(song_name):
    devices = sp.devices()

    if not devices["devices"]:
        print("No Spotify devices found")
        return False

    # Prefer desktop/computer device
    device = next(
        (d for d in devices["devices"] if d["type"] == "Computer"),
        devices["devices"][0]
    )

    device_id = device["id"]

    results = sp.search(q=song_name, type="track", limit=1)

    if not results["tracks"]["items"]:
        return False

    track_uri = results["tracks"]["items"][0]["uri"]

    sp.start_playback(
        device_id=device_id,
        uris=[track_uri]
    )

    return True
