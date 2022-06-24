from typing import Iterable
from bisect import bisect_left


from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison
from devolving_music.lib.score_object import ScoreObject

import pdb 
#use for debugging
# pdb.set_trace()

class SongScores():
    def __init__(self, event: Event):
        # self.song_submissions = SongSubmission.get_voteable_submissions(Event)
        self.song_submissions = SongSubmission.get_voteable_submissions_dict(event)
        self.comparison_submissions = SongComparison.get_event_comparisons(event)

    @staticmethod
    def compare_logged(comparison_submission: "SongComparison", song1: "ScoreObject", song2: "ScoreObject"):
        return not song1.compare_present(comparison_submission) and not song2.compare_present(comparison_submission)

    @staticmethod
    def update_song_rating(comparison_submission: "SongComparison", song1: "ScoreObject", song2: "ScoreObject", score_range=30):
        if SongScores.compare_logged(comparison_submission, song1, song2):
            song1.log_comparison(comparison_submission)
            song2.log_comparison(comparison_submission)
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


    def get_scores(self):
        #song_submissions song_submissions should be a list of
        # song submissions ordered from least to greatest
        # by songsubmission id
        for compare in self.comparison_submissions:
            song1_index=compare.first_submission.id
            song2_index=compare.second_submission.id
            song1 = self.song_submissions[song1_index]
            song2 = self.song_submissions[song2_index]
            self.song_submissions[song1_index], self.song_submissions[song2_index] = \
                SongScores.update_song_rating(compare, song1, song2)
            #pdb.set_trace()
        return self.song_submissions
