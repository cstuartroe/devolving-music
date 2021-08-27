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
