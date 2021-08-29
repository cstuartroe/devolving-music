from django.db import models
from django.utils import timezone
from .event import Event
from .song import Song


class SongSubmission(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_event_and_song",
                fields=[
                    "event",
                    "song",
                ],
            )
        ]

    @staticmethod
    def submit(song: Song, event: Event):
        try:
            sub = SongSubmission.objects.get(
                event=event,
                song=song,
            )
        except SongSubmission.DoesNotExist:
            sub = SongSubmission(
                event=event,
                song=song,
                created_at=timezone.now(),
            )
            sub.save()

        return sub
