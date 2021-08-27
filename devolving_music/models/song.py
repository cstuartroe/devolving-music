from django.db import models
from .artist import Artist


class Song(models.Model):
    title = models.CharField(max_length=64)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    platform_id = models.CharField(max_length=32, unique=True)
