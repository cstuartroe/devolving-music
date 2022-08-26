from django.db import models
from .artist import Artist


class Event(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField()
    created_at = models.DateTimeField()
    image = models.CharField(max_length=128)
    visible = models.BooleanField()
    allow_spotify = models.BooleanField()
    allow_youtube = models.BooleanField()
    allow_soundcloud = models.BooleanField()

    @staticmethod
    def disallowed_platform_message(platform: Artist.MusicPlatform):
        return f"{platform.value} submissions not permitted for this event."

    def __str__(self):
        return f"Event {repr(self.name)}"
