from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from devolving_music.models.event import Event
from devolving_music.lib.song_scores import SongScores
from .param_utils import success, safe_url_params


class CurrentPlaylist(LoginRequiredMixin, View):
    @safe_url_params
    def get(self, _request, event: Event):
        return success([
            score.to_json()
            for score in SongScores(event).get_final_list()
        ])
