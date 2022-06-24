from bisect import bisect_left

from typing import Iterable


from django.db import models


from .song import Song

from devolving_music.lib.elo_scoring import elo_rating


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
