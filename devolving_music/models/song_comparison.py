from django.db import models
from django.contrib.auth.models import User
from .song_submission import SongSubmission
from .serializers import user_to_json


class SongComparison(models.Model):
    first_submission = models.ForeignKey(SongSubmission, on_delete=models.CASCADE, related_name='+')
    second_submission = models.ForeignKey(SongSubmission, on_delete=models.CASCADE, related_name='+')
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    first_better = models.BooleanField()
    first_peakier = models.BooleanField()
    first_post_peakier = models.BooleanField()

    def __str__(self):
        return (f"{self.voter.first_name} compared {repr(self.first_submission.song.title)} and "
                f"{repr(self.second_submission.song.title)}")

    def to_json(self):
        return {
            "id": self.id,
            "first_submission": self.first_submission.to_json(),
            "second_submission": self.second_submission.to_json(),
            "voter": user_to_json(self.voter),
            "created_at": self.created_at,
            "first_better": self.first_better,
            "first_peakier": self.first_peakier,
            "first_post_peakier": self.first_post_peakier,
        }

