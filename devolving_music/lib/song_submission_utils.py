from django.utils import timezone
from devolving_music.models.event import Event
from devolving_music.models.song import Song
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.duplication_flag import DuplicationFlag


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


def submit_song(song: Song, event: Event) -> SongSubmission:
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
        _check_duplicates(sub)

    return sub
