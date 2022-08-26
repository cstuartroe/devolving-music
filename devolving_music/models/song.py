from django.db import models
from devolving_music.lib.language import fuzzy_match
from .artist import Artist


class Song(models.Model):
    title = models.CharField(max_length=128)
    artists = models.ManyToManyField(Artist)
    platform_id = models.CharField(max_length=32, unique=True)

    @staticmethod
    def from_fields(platform_id: str, title: str, artists: list):
        try:
            song = Song.objects.get(platform_id=platform_id)
        except Song.DoesNotExist:
            song = Song(platform_id=platform_id)

        song.title = title
        song.save()

        song.artists.set(artists)
        song.save()

        return song

    @staticmethod
    def from_spotify_json(data):
        artists = [
            Artist.from_fields(artist_data["id"], artist_data["name"], Artist.MusicPlatform.SPOTIFY)
            for artist_data in data["artists"]
        ]

        return Song.from_fields(data["id"], data["name"], artists)

    @staticmethod
    def from_youtube_json(data):
        artist = Artist.from_fields(
            data["snippet"]["channelId"],
            data["snippet"]["channelTitle"],
            Artist.MusicPlatform.YOUTUBE,
        )

        return Song.from_fields(data["id"], data["snippet"]["title"], [artist])

    @staticmethod
    def fuzzy_match(song1: "Song", song2: "Song") -> bool:
        return fuzzy_match(song1.title, song2.title)

    def __str__(self):
        return f"{repr(self.title)} by {self.artists.all()[0]}"
