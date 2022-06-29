from django.views import View

from devolving_music.lib.score_object import ScoreSuite
from devolving_music.lib.song_scores import SongScores
from .param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.models.song_submission import SongSubmission


class GetSongPairView(View):
    @safe_url_params
    def get(self, _request, event: Event):

        voteable_submissions = ScoreSuite.get_voteable_submissions(event)

        if len(voteable_submissions) < 2:
            return failure("Not enough songs have been submitted for this event.")

        Scores = SongScores(event)
        Scores_list = Scores.get_scores()
        info_list = SongScores.get_info_sort(Scores_list)
        sub2_id = Scores.get_compare_submission_linear(info_list[0])


        #grab submission with least ammount of information
        sub1 = SongSubmission.objects.get(id = info_list[0])
        #grab random submission
        sub2 = SongSubmission.objects.get(id = sub2_id)

        return success({
            "sub1": SongSubmissionSerializer(sub1).data,
            "sub2": SongSubmissionSerializer(sub2).data,
            "color1": get_song_color(sub1.song),
            "color2": get_song_color(sub2.song),
        })
