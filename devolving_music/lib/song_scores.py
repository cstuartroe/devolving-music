from typing import Iterable
from bisect import bisect_left


from devolving_music.lib.elo_scoring import elo_rating


from devolving_music.models.event import Event


from devolving_music.models.song_submission import SongSubmission


from devolving_music.models.song_comparison import SongComparison


from devolving_music.lib.score_object import ScoreSuite


class SongScores():

    def __init__(self, event: Event):

        self.song_submissions = ScoreSuite.get_song_scores_dict(event)

        self.comparison_submissions = ScoreSuite.get_event_comparisons(event)

    @staticmethod
    def compare_not_found(
            comparison_submission: "SongComparison",
            song1: "ScoreObject",
            song2: "ScoreObject"):

        return not song1.compare_present(
            comparison_submission) and not song2.compare_present(comparison_submission)

    @staticmethod
    def update_song_rating(
            comparison_submission: "SongComparison",
            song1: "ScoreObject",
            song2: "ScoreObject",
            score_range=30):

        if SongScores.compare_not_found(comparison_submission, song1, song2):

            song1.log_comparison(comparison_submission)

            song2.log_comparison(comparison_submission)

            song1.quality_score, song2.quality_score = elo_rating(
                song1.quality_score, song2.quality_score, score_range, comparison_submission.first_better)

            song1.energy_score, song2.energy_score = elo_rating(
                song1.energy_score, song2.energy_score, score_range, comparison_submission.first_peakier)

            song1.post_peak_score, song2.post_peak_score = elo_rating(
                song1.post_peak_score, song2.post_peak_score, score_range, comparison_submission.first_post_peakier)

        else:
            pass

    def get_scores(self):

        # song_submissions song_submissions should be a list of

        # song submissions ordered from least to greatest

        # by songsubmission id

        for compare in self.comparison_submissions:

            song1_index = compare.first_submission.id

            song2_index = compare.second_submission.id

            song1 = self.song_submissions[song1_index]

            song2 = self.song_submissions[song2_index]

            SongScores.update_song_rating(compare, song1, song2)

        return self.song_submissions

    @staticmethod
    def get_info_sort(song_submissions_scored: Iterable["SongSubmission"]):

        info_submissions = []

        # sort by info_submissions=song_submissions_scored.info
        return info_submissions

    @staticmethod
    def get_energy_sort(song_submissions_scored: Iterable["SongSubmission"]):

        # song_submissions_scored is a list of song submissions

        # that have been scored with current comparisons

        # return song submission sorted from energy least to greatest

        # complete this

        # sorts by energy
        return song_submissions_scored

    @staticmethod
    def get_peak_sort(song_submissions_scored: Iterable["SongSubmission"]):

        # song_submissions_scored is a list of song submissions

        # that have been scored with current comparisons

        # sorts by peakyness
        return song_submissions_scored

    @staticmethod
    def mvg_avg(song_submissions_sorted: Iterable["SongSubmission"]):

        mvg_avg = [None] * len(song_submissions_sorted)

        # song_submissions_scored is a list of song submissions

        # that have been sorted into prepeak,peak,and post peak

        # these prepeak, peak, and post posteak have each been sorted
        # accordingly with energy

        # that have been scored with current comparisons

        # get a moving average corresponding to quality score

        return mvg_avg

    @staticmethod
    def check_quality(
            song_submissions_sorted: Iterable["SongSubmission"],
            remove: int):

        song_submissions_pruned = song_submissions_sorted

        # do (song_submissions_sorted[i].quality_score - mvg_avg[i])

        # for every song in score submission

        # return n indices with smallest values

        # these indices are to be removed
        return song_submissions_pruned

    @staticmethod
    def get_final_list(comparison_submissions: Iterable["SongComparison"],


                       song_submissions: Iterable["SongSubmission"]):

        scored_submissions = SongSubmission.get_scores(
            comparison_submissions, song_submissions)

        # remove all song_submissions with no information

        # sort by peakyness

        # peaky_sorted_submissions=get_peak_sort(scored_submissions)

        # Break peaky_sorted into two bing  pre peak and post peak

        # energy_sorted=[get_energy_sort(prepeak),reverse(get_energy_sort(postpeak))]

        # final_list = energy_sorted

        final_list = []
        return final_list

    def get_quality_list(
            final_list: Iterable["SongSubmission"],
            length_limit=300):

        final_quality_list = []

        # if len(final_list) is above length limit

        # remove_index=check_quality(final_list,len(energy_sorted)-lengthlimit)

        # final_quality_list=remove(energy_sorted,remove_index)

        return final_quality_list
