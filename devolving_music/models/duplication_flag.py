from django.db import models
from django.utils.translation import gettext_lazy as _
from .song_submission import SongSubmission


class DuplicationFlag(models.Model):
    """This model is written to operate on song submissions rather than songs
       because different judgements may be warranted for different events.
    """

    class Status(models.TextChoices):
        UNREVIEWED = "unreviewed", _("unreviewed")
        UNRELATED = "unrelated", _("unrelated")
        DIFFERENT_VERSIONS = "different_versions", _("different_versions")
        DUPLICATE = "duplicate", _("duplicate")

    existing_submission = models.ForeignKey(
        SongSubmission,
        on_delete=models.CASCADE,
        related_name="possible_subsequent_duplicates",
    )
    new_submission = models.ForeignKey(
        SongSubmission,
        on_delete=models.CASCADE,
        related_name="possible_prior_duplicates",
    )
    status = models.CharField(max_length=20, choices=Status.choices)
    reviewed_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_submission_pair",
                fields=[
                    "existing_submission",
                    "new_submission",
                ],
            )
        ]
