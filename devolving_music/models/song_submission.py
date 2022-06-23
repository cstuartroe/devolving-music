from typing import Iterable
from django.db import models
from .event import Event
from .song import Song
from devolving_music.lib.elo_scoring import elo_rating
from django.utils.functional import cached_property
from bisect import bisect_left

class SongSubmission(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.energy_score = None
        self.quality_score=None
        self.post_peak_score=None
        self.counted_compares=[]

    @property
    def info_score(self):
        return len(self.counted_compares)


    def update_info(self,comparison):
        self.counted_compares.append(comparison.id)

    def compare_present(self,comparison):
        return comparison.id in self.counted_compares

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
    def check_compare(comparison_submission:"SongComparison",\
        song1:"SongSubmission",song2:"SongSubmission"):
        return not song1.compare_present(comparison_submission) and \
        not song2.compare_present(comparison_submission)

    @staticmethod
    def elo_song_rating(comparison_submission:"SongComparison",song1,song2,score_range=30):
        if SongSubmission.check_compare(comparison_submission,song1,song2):
            song1.update_info(comparison_submission)
            song2.update_info(comparison_submission)
            song1.quality_score,song2.quality_score=\
                elo_rating(song1.quality_score,song2.quality_score,\
                score_range,comparison_submission.first_better)
            song1.energy_score,song2.energy_score=\
                elo_rating(song1.energy_score,song2.energy_score,\
                score_range,comparison_submission.first_peakier)
            song1.post_peak_score,song2.post_peak_score=\
                elo_rating(song1.post_peak_score,song2.post_peak_score,\
                score_range,comparison_submission.first_post_peakier)
            return song1,song2
        else:
            return song1,song2

    @staticmethod
    def submission_index(song_submissions:Iterable["SongSubmission"], song:"SongSubmission"):
        song_submissions=list(sub.id for sub in song_submissions)
        song=song.id
        'Locate the leftmost value exactly equal to x'
        i = bisect_left(song_submissions, song)
        if i != len(song_submissions) and song_submissions[i] == song:
            return i
        raise ValueError

    @staticmethod
    def find_submission_index(compare:"SongComparison",song_submissions:Iterable["SongSubmission"]):
        song_index_1=SongSubmission.submission_index(song_submissions,compare.first_submission)
        song_index_2=SongSubmission.submission_index(song_submissions,compare.second_submission)
        return  song_index_1,song_index_2

    @staticmethod
    def get_scores(comparison_submissions:Iterable["SongComparison"],\
        song_submissions:Iterable["SongSubmission"]):
        #song_submissions song_submissions should be a list of
        # song submissions ordered from least to greatest
        # by songsubmission id
        for compare in comparison_submissions:
            song1_index,song2_index=SongSubmission.find_submission_index(compare,song_submissions)
            song1=song_submissions[song1_index]
            song2=song_submissions[song2_index]
            song_submissions[song1_index],song_submissions[song2_index]=\
                SongSubmission.elo_song_rating(compare,song1,song2)
        return song_submissions
