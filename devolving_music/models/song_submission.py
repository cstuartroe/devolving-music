from typing import Iterable
from django.db import models
from .event import Event
from .song import Song
from devolving_music.lib.elo_scoring import elo_rating
from django.utils.functional import cached_property
class SongSubmission(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    def __init__(self, *args, **kwargs):
        self.energy_score = 0
        self.quality_score=0
        self.post_peak_score=0
        self._counted_compares=[]
        self._info_score=len(self._counted_compares)
        super().__init__(*args, **kwargs)
    
    def update_info(self,comparison):
        self._counted_compares.append(comparison.id)
        self._info_score=len(self._counted_compares)
    def compare_present(self,comparison):
        return comparison.id in self._counted_compares

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
                for sub in SongSubmission.objects.filter(event__exact=Event).order_by('created_at')
                if sub.voteable()
            ]
        return voteable_submissions
    @staticmethod
    def check_compare(comparison_submission:"SongComparison"):
        song1=comparison_submission.first_submission
        song2=comparison_submission.second_submission
        return not song1.compare_present(comparison_submission) and \
        not song2.compare_present(comparison_submission)

    @staticmethod
    def elo_song_rating(comparison_submission:"SongComparison", score_range=30):
        song1id=comparison_submission.first_submission.id
        song2id=comparison_submission.second_submission.id
        song1=SongSubmission.objects.get(id=song1id)
        song2=SongSubmission.objects.get(id=song2id)
        if(SongSubmission.check_compare(comparison_submission)):
            song1.update_info(comparison_submission)
            song2.update_info(comparison_submission)
            song1.quality_score,song2.quality_score=elo_rating(song1.quality_score,song2.quality_score,\
                score_range,comparison_submission.first_better)
            song1.energy_score,song2.energy_score=elo_rating(song1.energy_score,song2.energy_score,\
                score_range,comparison_submission.first_peakier)
            song1.post_peak_score,song2.post_peak_score=elo_rating(song1.post_peak_score,song2.post_peak_score,\
                score_range,comparison_submission.first_post_peakier)
            
            return True
        else:
            return False
    @staticmethod
    def get_scores(comparison_submissions:Iterable["SongComparison"]):
        for compare in comparison_submissions:
            SongSubmission.elo_song_rating(compare)
