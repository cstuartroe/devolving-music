from django.views import View
from .param_utils import safe_url_params, success, failure
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer


class GetSongPairView(View):
    @safe_url_params
    def get(self, _request, event: Event):
        event_submissions = SongSubmission.objects.filter(event__exact=event).order_by('?')

        try:
            return success({
                "sub1": SongSubmissionSerializer(event_submissions[0]).data,
                "sub2": SongSubmissionSerializer(event_submissions[0]).data,
            })
        except IndexError:
            return failure("Not enough songs have been submitted for this event.")
