from math import inf
from typing import List
import random
import copy

from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison
from devolving_music.lib.score_suite import ScoreSuite

PEAK_PROPORTION = 0.7
INFO_THRESHOLD = 1


class SongScores():

    def __init__(self, event: Event):
        self._song_score_dict = ScoreSuite.get_song_scores_dict(event)
        self.comparison_submissions = ScoreSuite.get_event_comparisons(event)
        self.update_scores()

    def update_scores(self) -> "None":
        # calculates scores for all submissions using current comparisons
        # returns a dictionary where keys are the song submission id
        # corresponding to the score suite object
        for compare in self.comparison_submissions:
            song_suite_1 = self._song_score_dict[compare.first_submission.id]
            song_suite_2 = self._song_score_dict[compare.second_submission.id]

            SongScores.update_song_rating(compare, song_suite_1, song_suite_2)

    @property
    def scores_list(self) -> "list[ScoreSuite]":
        # calculates scores for all submissions using current comparisons
        # returns list of all score suite objects
        return list(self.scores_dict.values())

    @property
    def scores_dict(self) -> "dict[int, ScoreSuite]":
        # calculates scores for all submissions using current comparisons
        # returns list of all score suite objects
        return self._song_score_dict

    def get_compare_submission_random(self, submission_id) -> SongSubmission:
        key_list = list(self.scores_dict.keys())
        key_list.remove(submission_id)
        return self.scores_dict.get(
            random.choice(key_list)).song_submission

    def get_compare_submission_closest(self, score_suite_obj: "ScoreSuite", information_threshold : int) -> List["ScoreSuite"]:
        # information threshold is the threshhold at which we start to consider score_suites as being able to be close to score_suite_obj
        # score_suites below this information threshhold are considered to be infinitely far away from score_suite_obj
        score_dict = {**self.scores_dict}
        target_id = score_suite_obj.song_submission.id
        score_dict.pop(target_id)
        score_list = list(score_dict.values())
        closest_songs = SongScores.get_distance_sort(score_suite_obj, score_list, information_threshold)
        return closest_songs


    def get_compare_submission_linear(self, submission_id) -> SongSubmission:
        if (len(self.comparison_submissions) == 0):
            return self.get_compare_submission_random(submission_id)
        first_recent = self.comparison_submissions[-1].first_submission
        if (submission_id == first_recent.id):
            return self.get_compare_submission_random(submission_id)
        return first_recent

    def mvg_avg(
            self,
            song_submissions_sorted: List["ScoreSuite"]) -> List[int]:
        mvg_avg = [None] * len(song_submissions_sorted)

        # song_submissions_scored is a list of song submissions
        # that have been sorted into prepeak,peak,and post peak
        # these prepeak, peak, and post posteak have each been sorted
        # accordingly with energy
        # that have been scored with current comparisons
        # get a moving average corresponding to quality score

        return mvg_avg

    def check_quality(self,
                      song_submissions_sorted: List["ScoreSuite"],
                      remove: int) -> List["ScoreSuite"]:

        song_submissions_pruned = song_submissions_sorted

        # do (song_submissions_sorted[i].quality_score - mvg_avg[i])
        # for every song in score submission
        # return n indices with smallest values
        # these indices are to be removed

        return song_submissions_pruned

    def get_dict_from_keys(self, new_keys) -> "dict[int, ScoreSuite]":
        return {key: self.scores_dict[key] for key in new_keys}

    def get_final_list(self) -> List["ScoreSuite"]:

        scored_submissions = self.scores_list

        # remove all song_submissions with no information
        info_list = SongScores.get_info_sort(scored_submissions)

        informed_list = list(
            filter(
                lambda sub: sub.info_score >= INFO_THRESHOLD,
                info_list))

        # sort by postpeakyness
        peaky_list = SongScores.get_peak_sort(informed_list)
        peak_loc = int(PEAK_PROPORTION * len(peaky_list))
        # Break peaky_sorted into two bins pre peak and post peak
        pre_peak = peaky_list[:peak_loc]
        post_peak = peaky_list[peak_loc:]
        # energy_sorted
        comeup = SongScores.get_energy_sort(pre_peak)
        cooldown = SongScores.get_energy_sort(post_peak)
        cooldown = cooldown[::-1]

        # final_list is the song submission keys properly sorted
        final_list = comeup + cooldown

        return final_list

    def get_quality_list(self,
                         length_limit=300) -> List["ScoreSuite"]:

        final_quality_list = []

        # if len(final_list) is above length limit
        # remove_index=check_quality(final_list,len(energy_sorted)-lengthlimit)
        # final_quality_list=remove(energy_sorted,remove_index)

        return final_quality_list

    @staticmethod
    # sorts in ascending order
    def get_info_sort(
            score_suite_list: List["ScoreSuite"],
            get_informed=False,
            informed_threshold=1) -> List["ScoreSuite"]:
        """
        Returns a list of song suites ordered by low information songs with the lowest information score
        randomly shuffled before being added to the list

        """
        score_suite_list = sorted(score_suite_list, key=lambda sub: sub.info_score)
        rightend = 0

        if (not get_informed):
            informed_threshold = score_suite_list[0].info_score
        
        for sub in score_suite_list:
            sub_info = sub.info_score
            if sub_info <= informed_threshold:
                rightend += 1
            else:
                break
        other_info = score_suite_list[rightend:]
        if (get_informed):
            info_submissions = other_info
        else:
            lowest_info = score_suite_list[0:rightend]
            random.shuffle(lowest_info)
            info_submissions = lowest_info + other_info

        # return list of keys of dictionary of song objects sorted by info
        return info_submissions

    @staticmethod
    def weighted_lowest_info(
            score_suite_list: List["ScoreSuite"],
            luck_factor : int) -> "ScoreSuite":
        #this is a luck factor that determines how skewwed we are to low information songs
        # when luck factor goes to 0 we will only grab the lowest infromed song
        # when luck factor is 1 all songs have at some chance of being chosen while low informed songs are more likely 
        # when luck factor 1>> all songs have roughly equal chance of being chosen
        info_list = SongScores.get_info_sort(score_suite_list)
        ceiling = round(((info_list[-1].info_score) + 1) * luck_factor)

        random_num = 0
        for song_score in info_list:
            increase_random = ceiling - song_score.info_score
            if (increase_random > 0):
                random_num += increase_random
            else:
                break
        select_num = random.randrange(random_num + 1)
        ceiling_check = 0

        for song_score in info_list:
            increase_ceiling = ceiling - song_score.info_score
            if (increase_ceiling < 0):
                increase_ceiling = 0

            if ((ceiling_check + increase_ceiling) >= select_num):
                return song_score
            else:
                ceiling_check += increase_ceiling

    @staticmethod
    # sorts in ascending order
    def get_distance_sort(score_suite_obj: "ScoreSuite",
            score_suite_list: List["ScoreSuite"], info_threshold : int) -> List["ScoreSuite"]:
        score_suite_list = sorted(score_suite_list ,
            key=lambda sub: score_suite_obj.devolve_distance(sub) if sub.info_score >= info_threshold else inf)
        # return list of keys of dictionary of song objects sorted by energy
        return score_suite_list

    @staticmethod
    # sorts in ascending order
    def get_energy_sort(
            score_suite_list: List["ScoreSuite"]) -> List["ScoreSuite"]:
        score_suite_list = sorted(score_suite_list,
            key=lambda sub: sub.energy_score if sub.energy_score is not None else -inf)
        # return list of keys of dictionary of song objects sorted by energy
        return score_suite_list

    @staticmethod
    # sorts in ascending order
    def get_peak_sort(
            score_suite_list: List["ScoreSuite"]) -> List["ScoreSuite"]:
        score_suite_list = sorted(score_suite_list,
            key=lambda sub: sub.post_peak_score if sub.post_peak_score is not None else -
            inf)
        # return list of keys of dictionary of song objects sorted by energy
        return score_suite_list

    @staticmethod
    def compare_not_found(
            comparison_submission: "SongComparison",
            song1: "ScoreSuite",
            song2: "ScoreSuite") -> bool:

        return not song1.compare_present(
            comparison_submission) and not song2.compare_present(comparison_submission)

    @staticmethod
    def update_song_rating(
            comparison_submission: "SongComparison",
            song1: "ScoreSuite",
            song2: "ScoreSuite",
            score_range=30) -> None:

        if SongScores.compare_not_found(comparison_submission, song1, song2):

            song1.log_comparison(comparison_submission)

            song2.log_comparison(comparison_submission)

            song1.quality_score, song2.quality_score = elo_rating(
                song1.quality_score, song2.quality_score, score_range, comparison_submission.first_better)

            song1.energy_score, song2.energy_score = elo_rating(
                song1.energy_score, song2.energy_score, score_range, comparison_submission.first_peakier)

            song1.post_peak_score, song2.post_peak_score = elo_rating(
                song1.post_peak_score, song2.post_peak_score, score_range, comparison_submission.first_post_peakier)
