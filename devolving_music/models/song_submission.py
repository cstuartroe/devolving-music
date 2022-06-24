from bisect import bisect_left
from typing import Iterable

from django.db import models

from .song import Song
from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.lib.score_object import ScoreObject
from .event import Event

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

    def voteable(self) -> bool:
        for flag in self.possible_prior_duplicates.all():
            if flag.blocks_voting():
                return False

        return True

    @staticmethod
    def get_voteable_submissions(Event):
        voteable_submissions = [
                sub
                for sub in SongSubmission.objects.filter(event__exact=Event).order_by('id')
                if sub.voteable()
            ]
        return voteable_submissions

    @staticmethod
    def get_voteable_submissions_dict(Event):
        song_subs = SongSubmission.get_voteable_submissions(Event)
        score_objects = list(ScoreObject(sub) for sub in song_subs)
        song_subs_id = list(sub.id for sub in song_subs)
        voteable_submissions_dict = dict(zip(song_subs_id , score_objects))
        return voteable_submissions_dict
