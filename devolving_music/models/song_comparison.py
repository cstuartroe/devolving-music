from django.db import models
from .song_submission import SongSubmission


class SongComparison(models.Model):
    first_submission = models.ForeignKey(SongSubmission, on_delete=models.CASCADE, related_name='+')
    second_submission = models.ForeignKey(SongSubmission, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField()
    first_better = models.BooleanField()
    first_peakier = models.BooleanField()
    first_post_peakier = models.BooleanField()

