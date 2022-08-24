from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from devolving_music.lib.score_suite import ScoreSuite
from devolving_music.lib.song_scores import SongScores
from .param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
INFORMED = 0

class GetSongPairView(LoginRequiredMixin, View):
    @safe_url_params
    def get(self, _request, event: Event):

        voteable_submissions = ScoreSuite.get_voteable_submissions(event)

        if len(voteable_submissions) < 2:
            return failure(
                "Not enough songs have been submitted for this event.")

        scores = SongScores(event)
        scores_list = scores.get_scores_list()

        # grab submission with a tendency to be low information
        score_low_info = SongScores.weighted_lowest_info(scores_list)
        sub1 = score_low_info.song_submission
        # grab random submission if song is uninformed else grab the song closest in devolving space  
        if(score_low_info.info_score >= INFORMED):
            close_songs = scores.get_compare_submission_closest(score_low_info, INFORMED)
            closest_song = close_songs[0]
            sub2= closest_song.song_submission
        else:
            sub2 = scores.get_compare_submission_random(sub1.id)

        return success({
            "sub1": SongSubmissionSerializer(sub1).data,
            "sub2": SongSubmissionSerializer(sub2).data,
            "color1": get_song_color(sub1.song),
            "color2": get_song_color(sub2.song),
        })
