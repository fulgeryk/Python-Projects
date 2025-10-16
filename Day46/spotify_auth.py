import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()
class SPOTIFY:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id = os.environ.get("CLIENT_ID"),
            client_secret = os.environ.get("CLIENT_SECRET"),
            redirect_uri = "https://example.com/callback",
            scope = "playlist-modify-private",
            username = "Fulger"
        ))
        self.user = self.sp.current_user()["id"]
