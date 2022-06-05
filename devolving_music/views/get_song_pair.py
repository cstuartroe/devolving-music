from django.views import View
from .param_utils import safe_url_params, success, failure
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer


class GetSongPairView(View):
    @safe_url_params
    def get(self, _request, event: Event):
        if SongSubmission.objects.count() < 2:
            sub1, sub2 = SongSubmission.objects.filter(event__exact=event).order_by('?')[:2]

            return success({
                "sub1": SongSubmissionSerializer(sub1).data,
                "sub2": SongSubmissionSerializer(sub2).data,
            })
        else:
            return failure("Not enough songs have been submitted for this event.")
