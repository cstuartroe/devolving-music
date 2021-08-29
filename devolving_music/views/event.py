from django.views import View
from devolving_music.models import Event
from devolving_music.models.serializers import EventSerializer
from ._utils import safe_url_params


class EventView(View):
    PATH = "events/<int:event>"

    @safe_url_params
    def get(self, _request, event: Event):
        return EventSerializer(event).data
