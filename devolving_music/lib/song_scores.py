from cmath import inf
from typing import Iterable
import random


from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison
from devolving_music.lib.score_object import ScoreSuite


class SongScores():

    def __init__(self, event: Event):
        self.song_score_dict = ScoreSuite.get_song_scores_dict(event)
        self.comparison_submissions = ScoreSuite.get_event_comparisons(event)

    def get_scores(self):
        #calculates scores for all submissions using current comparisons
        for compare in self.comparison_submissions:
            song1_index = compare.first_submission.id
            song2_index = compare.second_submission.id
            song1 = self.song_score_dict[song1_index]
            song2 = self.song_score_dict[song2_index]

            SongScores.update_song_rating(compare, song1, song2)

        return self.song_score_dict
    
    def get_compare_submission_random(self, submission_key):
        key_list = list(self.song_score_dict.keys())
        key_list.remove(submission_key)
        # once you have a critical number of comparisons then pull from quality list
        return random.choice(key_list)

    def get_compare_submission_linear(self, submission_key):
        compare_list = self.comparison_submissions
        if(len(compare_list)==0):
            return self.get_compare_submission_random(submission_key)
        first_sub_id=compare_list[-1].first_submission.id
        if(submission_key==first_sub_id):
            return self.get_compare_submission_random(submission_key)
        return first_sub_id

        # once you have a critical number of comparisons then pull from quality list
        return random.choice(key_list)



    def mvg_avg(self,song_submissions_sorted: Iterable["SongSubmission"]):
        mvg_avg = [None] * len(song_submissions_sorted)

        # song_submissions_scored is a list of song submissions
        # that have been sorted into prepeak,peak,and post peak
        # these prepeak, peak, and post posteak have each been sorted
        # accordingly with energy
        # that have been scored with current comparisons
        # get a moving average corresponding to quality score

        return mvg_avg

    def check_quality(self,
            song_submissions_sorted: Iterable["SongSubmission"],
            remove: int):

        song_submissions_pruned = song_submissions_sorted

        # do (song_submissions_sorted[i].quality_score - mvg_avg[i])
        # for every song in score submission
        # return n indices with smallest values
        # these indices are to be removed

        return song_submissions_pruned

    def get_dict_from_keys(self, new_keys):
        new_dict=dict()
        new_dict={key: self.song_score_dict[key] for key in new_keys}
        return new_dict
    
    def get_final_list(self):

        scored_submissions = self.get_scores().copy()
        
        # remove all song_submissions with no information
        info_list = SongScores.get_info_sort(scored_submissions)
        for sub_info in info_list:
            i_score = scored_submissions[sub_info].info_score
            if(i_score == 0):
                del scored_submissions[sub_info]
            else:
                break
        # sort by postpeakyness
        peaky_list = SongScores.get_peak_sort(scored_submissions)
        peak_loc = int(0.7*len(peaky_list))
        # Break peaky_sorted into two bins pre peak and post peak
        pre_peak = self.get_dict_from_keys(peaky_list[:peak_loc])
        post_peak = self.get_dict_from_keys(peaky_list[peak_loc:])
        # energy_sorted
        comeup = SongScores.get_energy_sort(pre_peak)
        cooldown = SongScores.get_energy_sort(post_peak)
        cooldown = cooldown[::-1]

        # final_list is the song submission keys properly sorted
        final_list = comeup + cooldown

        return final_list

    def get_quality_list(self,
            length_limit=300):

        final_quality_list = []

        # if len(final_list) is above length limit 
        # remove_index=check_quality(final_list,len(energy_sorted)-lengthlimit)
        # final_quality_list=remove(energy_sorted,remove_index)

        return final_quality_list

    ###
    # static methods can be moved into helper function
    ###
    @staticmethod
    #sorts in ascending order
    def get_info_sort(song_dict: "dict[int, ScoreSuite]"):
        info_submissions = sorted(song_dict,key=lambda sub: song_dict.get(sub).info_score)
        # return list of keys of dictionary of song objects sorted by info
        return info_submissions

    @staticmethod
    #sorts in ascending order
    def get_energy_sort(song_dict: "dict[int, ScoreSuite]"):
        energy_submissions = sorted(song_dict,key=lambda sub: song_dict.get(sub).energy_score if song_dict.get(sub).energy_score is not None else -inf)
        # return list of keys of dictionary of song objects sorted by energy
        return energy_submissions
        
    @staticmethod
    #sorts in ascending order
    def get_peak_sort(song_dict: "dict[int, ScoreSuite]"):
        peak_submissions = sorted(song_dict,key=lambda sub: song_dict.get(sub).post_peak_score  if song_dict.get(sub).post_peak_score is not None else -inf)
        # return list of keys of dictionary of song objects sorted by peakyness
        return peak_submissions

    @staticmethod
    def compare_not_found(
            comparison_submission: "SongComparison",
            song1: "ScoreObject",
            song2: "ScoreObject"):

        return not song1.compare_present(comparison_submission) and not song2.compare_present(comparison_submission)

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

