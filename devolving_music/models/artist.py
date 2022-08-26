from django.db import models
from django.utils.translation import gettext_lazy as _


class Artist(models.Model):
    class MusicPlatform(models.TextChoices):
        SPOTIFY = 'Spotify', _('Spotify')
        YOUTUBE = 'YouTube', _('YouTube')
        SOUNDCLOUD = 'Soundcloud', _('Soundcloud')

    name = models.CharField(max_length=64)
    platform = models.CharField(
        max_length=16,
        choices=MusicPlatform.choices,
    )
    platform_id = models.CharField(max_length=32, unique=True)

    @staticmethod
    def from_fields(platform_id: str, name: str, platform: MusicPlatform):
        try:
            artist = Artist.objects.get(platform_id=platform_id)
        except Artist.DoesNotExist:
            artist = Artist(platform_id=platform_id)

        artist.name = name
        artist.platform = platform

        artist.save()

        return artist

    def __str__(self):
        return f"{self.name} on {self.platform}"
