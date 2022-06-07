from devolving_music.models.artist import Artist
from devolving_music.models.song import Song
from .spotify import get_spotify_embed_color


def get_color_from_title(title: str):
    return bytes(title + "   ", encoding="utf-8").hex()[:6]


def get_song_color(song: Song):
    platform = song.artists.first().platform

    if platform == Artist.MusicPlatform.SPOTIFY:
        return get_spotify_embed_color(song.platform_id)

    else:
        return get_color_from_title(song.title)
