from math import inf

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from devolving_music.lib.score_suite import ScoreSuite
from devolving_music.lib.song_scores import SongScores
from .param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer

LUCK_FACTOR = .4


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

        # grab submission with a tendency to be low information
        score_low_info = scores.weighted_lowest_info(LUCK_FACTOR)
        sub1 = score_low_info.song_submission
        # grab random submission if song is uninformed else grab the song closest in devolving space
        sub2 = scores.get_compare_submission_random(score_low_info).song_submission
        if score_low_info.info_score >= median_info:
            closest_song = scores.get_compare_submission_closest(score_low_info, median_info)
            if score_low_info.devolve_distance(closest_song) != inf:
                sub2 = closest_song.song_submission

        return success({
            "sub1": SongSubmissionSerializer(sub1).data,
            "sub2": SongSubmissionSerializer(sub2).data,
            "color1": get_song_color(sub1.song),
            "color2": get_song_color(sub2.song),
        })
