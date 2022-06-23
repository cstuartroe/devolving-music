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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.energy_score = None
        self.quality_score = None
        self.post_peak_score = None
        self.counted_compares = set()

    @property
    def info_score(self):
        return len(self.counted_compares)

    def update_info(self, comparison):
        self.counted_compares.add(comparison.id)

    def compare_present(self, comparison):
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
    def check_compare(comparison_submission: "SongComparison",
        song1: "SongSubmission", song2: "SongSubmission"):
        return not song1.compare_present(comparison_submission) and \
            not song2.compare_present(comparison_submission)

    @staticmethod
    def elo_song_rating(comparison_submission: "SongComparison", song1, song2, score_range=30):
        if SongSubmission.check_compare(comparison_submission, song1, song2):
            song1.update_info(comparison_submission)
            song2.update_info(comparison_submission)
            song1.quality_score, song2.quality_score = \
                elo_rating(song1.quality_score, song2.quality_score,
                score_range, comparison_submission.first_better)
            song1.energy_score, song2.energy_score = \
                elo_rating(song1.energy_score, song2.energy_score,
                score_range, comparison_submission.first_peakier)
            song1.post_peak_score, song2.post_peak_score = \
                elo_rating(song1.post_peak_score, song2.post_peak_score,
                score_range, comparison_submission.first_post_peakier)
            return song1, song2
        else:
            return song1, song2

    def submission_index(self, song_subs: Iterable["SongSubmission"]):
        song_submissions = list(sub.id for sub in song_subs)
        # Locate the leftmost value exactly equal to x
        i = bisect_left(song_submissions, self.id)
        if (i != len(song_submissions) and song_submissions[i] == self.id):
            return i
        raise ValueError

    @staticmethod
    def find_submission_index(compare: "SongComparison", song_submissions: Iterable["SongSubmission"]):
        song_index_1 = compare.first_submission.submission_index(song_submissions)
        song_index_2 = compare.second_submission.submission_index(song_submissions)
        return song_index_1, song_index_2

    @staticmethod
    def get_scores(comparison_submissions: Iterable["SongComparison"],song_submissions: Iterable["SongSubmission"]):
        #song_submissions song_submissions should be a list of
        # song submissions ordered from least to greatest
        # by songsubmission id
        for compare in comparison_submissions:
            song1_index, song2_index = SongSubmission.find_submission_index(compare,song_submissions)
            song1 = song_submissions[song1_index]
            song2 = song_submissions[song2_index]
            song_submissions[song1_index],song_submissions[song2_index]=\
                SongSubmission.elo_song_rating(compare, song1, song2)
        return song_submissions

    @staticmethod
    def get_info_sort(song_submissions_scored: Iterable["SongSubmission"]):
        info_submissions = []
        #sort by info_submissions=song_submissions_scored.info
        return info_submissions

    @staticmethod
    def get_energy_sort(song_submissions_scored: Iterable["SongSubmission"]):
        #song_submissions_scored is a list of song submissions
        # that have been scored with current comparisons
        #return song submission sorted from energy least to greatest
        #complete this
        #sorts by energy
        return song_submissions_scored

    @staticmethod
    def get_peak_sort(song_submissions_scored : Iterable["SongSubmission"]):
        #song_submissions_scored is a list of song submissions
        # that have been scored with current comparisons
        #sorts by peakyness
        return song_submissions_scored

    @staticmethod
    def mvg_avg(song_submissions_sorted:Iterable["SongSubmission"]):
        mvg_avg = [None]*len(song_submissions_sorted)
        #song_submissions_scored is a list of song submissions
        #that have been sorted into prepeak,peak,and post peak
        #these prepeak, peak, and post posteak have each been sorted accordingly with energy
        # that have been scored with current comparisons
        #get a moving average corresponding to quality score
        return mvg_avg

    @staticmethod
    def check_quality(song_submissions_sorted:Iterable["SongSubmission"],remove:int):
        song_submissions_pruned = song_submissions_sorted
        #do (song_submissions_sorted[i].quality_score - mvg_avg[i])
        # for every song in score submission
        # return n indices with smallest values 
        #these indices are to be removed 
        return song_submissions_pruned

    @staticmethod
    def get_final_list(comparison_submissions:Iterable["SongComparison"],
        song_submissions : Iterable["SongSubmission"]):
        scored_submissions = SongSubmission.get_scores(comparison_submissions, song_submissions)
        # remove all song_submissions with no information
        # sort by peakyness
        # peaky_sorted_submissions=get_peak_sort(scored_submissions)
        # Break peaky_sorted into two bing  pre peak and post peak
        # energy_sorted=[get_energy_sort(prepeak),reverse(get_energy_sort(postpeak))]
        # final_list = energy_sorted

        final_list = []
        return final_list

    def get_quality_list(final_list : Iterable["SongSubmission"],length_limit=300):
        final_quality_list = []
        # if len(final_list) is above length limit
        # remove_index=check_quality(final_list,len(energy_sorted)-lengthlimit)
        #final_quality_list=remove(energy_sorted,remove_index)
        return final_quality_list
