import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
import re

spotify_client = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(),
)
playlist_write_client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-modify-public"),
)


def get_song_data(playlist_id: str):
    offset = 0

    while True:
        res = spotify_client.playlist_items(
            playlist_id=playlist_id,
            fields="items(track(id, name, artists(id, name), is_local))",
            limit=100,
            offset=offset,
            additional_types=("track",),
        )

        yield from (item["track"] for item in res["items"])

        if len(res["items"]) == 0:
            break

        offset += 100


def add_songs(playlist_id: str, song_ids: list[str]):
    existing_items = spotify_client.playlist_items(playlist_id)['items']
    existing_track_ids = [
        item['track']['id']
        for item in existing_items
    ]
    playlist_write_client.playlist_remove_all_occurrences_of_items(playlist_id, existing_track_ids)
    playlist_write_client.playlist_add_items(playlist_id, song_ids)


def get_spotify_embed_color(platform_id: str):
    res = requests.get(f"https://open.spotify.com/embed/track/{platform_id}?utm_source=generator")

    return re.search(r"dominantColor%22%3A%22%23([\da-f]{6})", res.text).group(1)
