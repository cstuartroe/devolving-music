import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify_client = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(),
)
