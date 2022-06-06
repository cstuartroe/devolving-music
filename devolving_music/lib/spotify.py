import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import re

spotify_client = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(),
)


def get_embed_color(platform_id: str):
    res = requests.get(f"https://open.spotify.com/embed/track/{platform_id}?utm_source=generator")

    return re.search(r"dominantColor%22%3A%22%23([\da-f]{6})", res.text).group(1)
