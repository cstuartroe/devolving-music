from django.db import models
from django.contrib.auth.models import User
from .song_submission import SongSubmission


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

