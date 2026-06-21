import yaml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from io import BytesIO

with open("config.yaml") as f:
    _cfg = yaml.safe_load(f)["spotify"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=_cfg["client_id"],
    client_secret=_cfg["client_secret"],
    redirect_uri=_cfg["redirect_uri"],
    scope="user-read-currently-playing user-read-playback-state",
    cache_path=_cfg["cache_path"]
))


def fetch_album_art(url: str) -> Image.Image:
    resp = requests.get(url, timeout=5)
    img = Image.open(BytesIO(resp.content)).convert("RGB")
    return img.resize((16, 16), Image.LANCZOS)


def get_current_track():
    current = sp.current_playback()
    if current and current["is_playing"]:
        track = current["item"]
        return (
            track["id"],
            track["name"],
            track["artists"][0]["name"],
            track["album"]["images"][-1]["url"]
        )
    return None, None, None, None
