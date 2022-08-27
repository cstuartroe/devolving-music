from math import inf
import os

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from devolving_music.lib.score_suite import ScoreSuite
from devolving_music.lib.song_scores import SongScores
from .param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event

LUCK_FACTOR = .4
ABSOLUTE_INFO_THRESHOLD = 5


class GetSongPairView(LoginRequiredMixin, View):
    @safe_url_params
    def get(self, _request, event: Event):

        voteable_submissions = ScoreSuite.get_voteable_submissions(event)

        if len(voteable_submissions) < 2:
            return failure(
                "Not enough songs have been submitted for this event.")

        scores = SongScores.all_from_event(event).get_info_sort()

        # this is the threshold at which we consider a song informed
        # if we get an informed song we find another informed song that is close in devolve space
        median_info = scores[round(len(scores)/2.0)].info_score
        info_threshold = min(median_info, ABSOLUTE_INFO_THRESHOLD)

        # grab submission with a tendency to be low information
        score_low_info = scores.weighted_lowest_info(LUCK_FACTOR)
        # grab random submission if song is uninformed else grab the song closest in devolving space
        score2 = scores.get_compare_submission_random(score_low_info)
        if score_low_info.info_score >= info_threshold:
            similar_song = scores.get_compare_submission_closest(score_low_info, info_threshold)
            if score_low_info.devolve_distance(similar_song) != inf:
                score2 = similar_song

        return success({
            "score1": score_low_info.to_json(),
            "score2": score2.to_json(),
            "color1": get_song_color(score_low_info.song_submission.song),
            "color2": get_song_color(score2.song_submission.song),
            "showScores": bool(os.getenv("SHOW_SCORES")),
        })
