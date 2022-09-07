from django.db import models
from django.contrib.auth.models import User
from .song import Song
from .event import Event
from .serializers import user_to_json
from .serializers.event import EventSerializer


class SongSubmission(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def voteable(self) -> bool:
        for flag in self.possible_prior_duplicates.all():
            if flag.blocks_voting():
                return False

        return True

    def __str__(self):
        return f"{self.submitter.first_name} submitted {repr(self.song.title)} to {self.event}"

    def to_json(self):
        return {
            "id": self.id,
            "event": EventSerializer(self.event).data,
            "song": self.song.to_json(),
            "submitter": user_to_json(self.submitter),
            "created_at": self.created_at,
        }
