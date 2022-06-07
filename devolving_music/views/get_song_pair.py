from django.views import View
from .param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer


class GetSongPairView(View):
    @safe_url_params
    def get(self, _request, event: Event):
        queryset = SongSubmission.objects.filter(event__exact=event)

        if queryset.count() <= 2:
            return failure("Not enough songs have been submitted for this event.")

        sub1, sub2 = queryset.order_by('?')[:2]

        return success({
            "sub1": SongSubmissionSerializer(sub1).data,
            "sub2": SongSubmissionSerializer(sub2).data,
            "color1": get_song_color(sub1.song),
            "color2": get_song_color(sub2.song),
        })
