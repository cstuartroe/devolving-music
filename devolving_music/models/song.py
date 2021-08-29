from django.db import models
from .artist import Artist


class Song(models.Model):
    title = models.CharField(max_length=64)
    artists = models.ManyToManyField(Artist)
    platform_id = models.CharField(max_length=32, unique=True)

    @staticmethod
    def from_spotify_json(data):
        data = data["track"]

        artists = [
            Artist.from_spotify_json(artist_data)
            for artist_data in data["artists"]
        ]

        try:
            song = Song.objects.get(platform_id=data["id"])
        except Song.DoesNotExist:
            song = Song(platform_id=data["id"])

        song.title = data["name"]
        song.save()

        song.artists.set(artists)
        song.save()

        return song

