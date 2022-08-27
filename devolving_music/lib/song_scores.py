from math import inf
import random
from typing import Union

from devolving_music.models.event import Event
from devolving_music.lib.score_suite import ScoreSuite

PEAK_PROPORTION = 0.7
INFO_THRESHOLD = 1
DEFAULT_PLAYLIST_LENGTH = 100


class SongScores:

    def __init__(self, song_scores: list[ScoreSuite]):
        self._song_scores = song_scores

    def __getitem__(self, s: Union[slice, int]) -> Union["SongScores", ScoreSuite]:
        if isinstance(s, slice):
            return SongScores(self.scores_list.__getitem__(s))
        else:
            return self.scores_list[s]

    def __add__(self, other: "SongScores") -> "SongScores":
        return SongScores(self.scores_list + other.scores_list)

    def __len__(self):
        return len(self.scores_list)

    @classmethod
    def all_from_event(cls, event: Event):
        return cls(ScoreSuite.get_song_scores(event))

    @property
    def scores_list(self) -> list[ScoreSuite]:
        # calculates scores for all submissions using current comparisons
        # returns list of all score suite objects
        return self._song_scores

    def scores_excluding(self, score_suite: ScoreSuite):
        return [
            score
            for score in self.scores_list
            if score.song_submission.id != score_suite.song_submission.id
        ]

    def get_compare_submission_random(self, score_suite: ScoreSuite) -> ScoreSuite:
        return random.choice(self.scores_excluding(score_suite))

    def get_compare_submission_closest(self, from_score: ScoreSuite, information_threshold: int) -> ScoreSuite:
        # information threshold is the threshold at which we start to consider score_suites as being able to be close to score_suite_obj
        # score_suites below this information threshhold are considered to be infinitely far away from score_suite_obj
        closest_songs = self.get_distance_sort(from_score, information_threshold)
        return closest_songs[0]

    def moving_avg(self, song_submissions_sorted: list["ScoreSuite"]) -> list[int]:
        out = [None] * len(song_submissions_sorted)

        # song_submissions_scored is a list of song submissions
        # that have been sorted into prepeak,peak,and post peak
        # these prepeak, peak, and post posteak have each been sorted
        # accordingly with energy
        # that have been scored with current comparisons
        # get a moving average corresponding to quality score

        return out

    def check_quality(self,
                      song_submissions_sorted: list["ScoreSuite"],
                      remove: int) -> list["ScoreSuite"]:

        song_submissions_pruned = song_submissions_sorted

        # do (song_submissions_sorted[i].quality_score - mvg_avg[i])
        # for every song in score submission
        # return n indices with smallest values
        # these indices are to be removed

        return song_submissions_pruned

    def informed(self) -> "SongScores":
        return SongScores([
            sub
            for sub in self.scores_list
            if sub.info_score >= INFO_THRESHOLD
        ])

    def get_playlist_sort(self) -> "SongScores":
        # sort by postpeakyness
        peaky_list = self.informed().get_peak_sort()
        peak_loc = int(PEAK_PROPORTION * len(peaky_list))
        # Break peaky_sorted into two bins pre peak and post peak
        pre_peak = peaky_list[:peak_loc]
        post_peak = peaky_list[peak_loc:]
        # energy_sorted
        comeup = SongScores.get_energy_sort(pre_peak)
        cooldown = SongScores.get_energy_sort(post_peak)[::-1]

        return comeup + cooldown

    def get_final_list(self, length_limit=DEFAULT_PLAYLIST_LENGTH) -> "SongScores":
        out = self.get_playlist_sort().scores_list

        # if len(final_list) is above length limit
        # remove_index=check_quality(final_list,len(energy_sorted)-lengthlimit)
        # final_quality_list=remove(energy_sorted,remove_index)

        return SongScores(out)

    def get_info_sort(self, get_informed=False, informed_threshold=1) -> "SongScores":
        """
        Returns a list of song suites ordered by low information songs with the lowest information score
        randomly shuffled before being added to the list

        """
        score_suite_list = sorted(self.scores_list, key=lambda sub: sub.info_score)

        if not get_informed:
            informed_threshold = score_suite_list[0].info_score

        rightend = 0
        for sub in score_suite_list:
            if sub.info_score <= informed_threshold:
                rightend += 1
            else:
                break

        other_info = score_suite_list[rightend:]

        if get_informed:
            info_submissions = other_info
        else:
            lowest_info = score_suite_list[:rightend]
            random.shuffle(lowest_info)
            info_submissions = lowest_info + other_info

        return SongScores(info_submissions)

    def weighted_lowest_info(self, luck_factor: float) -> ScoreSuite:
        """Return a score suite at random, weighted towards lower information scores to a degree
           controlled by luck_factor.

           Args:
               luck_factor: A float determining how strongly low-information scores are favored.
                   - A luck_factor of 0 forces one of the scores tied for lowest information to be chosen.
                   - A luck_factor of less than 1 makes it impossible for the most-informed scores to be chosen.
                   - A luck_factor of 1 allows any score to be chosen, though low-information scores are likelier.
                   - As luck_factor increases past 1, the odds of choosing each score approaches equal.
        """
        info_list = self.get_info_sort().scores_list
        ceiling = round((info_list[-1].info_score + 1) * luck_factor)

        random_num = 0
        for song_score in info_list:
            increase_random = ceiling - song_score.info_score
            if increase_random > 0:
                random_num += increase_random
            else:
                break
        select_num = random.randrange(random_num + 1)
        ceiling_check = 0

        for song_score in info_list:
            increase_ceiling = ceiling - song_score.info_score
            if increase_ceiling < 0:
                increase_ceiling = 0

            if ceiling_check + increase_ceiling >= select_num:
                return song_score
            else:
                ceiling_check += increase_ceiling

    # sorts in ascending order
    def get_distance_sort(self, from_score: "ScoreSuite", info_threshold: int) -> "SongScores":
        score_suite_list = sorted(
            self.scores_list,
            key=lambda sub: from_score.devolve_distance(sub) if sub.info_score >= info_threshold else inf)
        return SongScores(score_suite_list)

    # sorts in ascending order
    def get_energy_sort(self) -> "SongScores":
        score_suite_list = sorted(
            self.scores_list,
            key=lambda sub: sub.energy_score if sub.energy_score is not None else -inf)
        return SongScores(score_suite_list)

    # sorts in ascending order
    def get_peak_sort(self) -> "SongScores":
        score_suite_list = sorted(
            self.scores_list,
            key=lambda sub: sub.post_peak_score if sub.post_peak_score is not None else -inf)
        return SongScores(score_suite_list)

