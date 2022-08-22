from typing import Iterable

from django.utils import timezone
from django.contrib.auth.models import User

from devolving_music.models.event import Event
from devolving_music.models.song import Song
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.duplication_flag import DuplicationFlag


SONG_SUBMISSION_QUOTA = 100


def _check_duplicates(sub: SongSubmission):
    for existing_sub in SongSubmission.objects.filter(event__exact=sub.event).exclude(id=sub.id):
        if Song.fuzzy_match(existing_sub.song, sub.song):
            flag = DuplicationFlag(
                existing_submission=existing_sub,
                new_submission=sub,
                status=DuplicationFlag.Status.UNREVIEWED,
                reviewed_at=None,
            )

            flag.save()


class QuotaExceededError(RuntimeError):
    pass


def submit_songs(songs: Iterable[Song], event: Event, submitter: User) -> list[SongSubmission]:
    to_submit = []
    submissions = []

    for song in songs:
        try:
            sub = SongSubmission.objects.get(
                event=event,
                song=song,
            )
            submissions.append(sub)

        except SongSubmission.DoesNotExist:
            to_submit.append(song)

    already_submitted_by_user = SongSubmission.objects.filter(submitter=submitter, event=event).count()

    if already_submitted_by_user + len(to_submit) > SONG_SUBMISSION_QUOTA:
        raise QuotaExceededError(f"Number of songs would exceed quota ({len(already_submitted_by_user)} songs "
                                 f"already submitted, currently attempting to submit {len(to_submit)} songs, "
                                 f"quota is {SONG_SUBMISSION_QUOTA}).")

    for song in to_submit:
        sub = SongSubmission(
            event=event,
            song=song,
            submitter=submitter,
            created_at=timezone.now(),
        )
        sub.save()
        _check_duplicates(sub)
        submissions.append(sub)

    return submissions
