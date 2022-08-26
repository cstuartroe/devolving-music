from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from devolving_music.models.event import Event
from devolving_music.lib.song_scores import SongScores
from .param_utils import safe_url_params, success


class ScoreSuitesView(LoginRequiredMixin, View):
    @safe_url_params
    def get(self, _request, event: Event):
        return success([
            score_suite.to_json()
            for score_suite in SongScores.all_from_event(event).scores_list
        ])
