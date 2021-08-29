from django.views import View
from django.utils import timezone
from datetime import date as dtdate
from devolving_music.models import Event
from devolving_music.models.serializers import EventSerializer
from ._utils import safe_url_params, safe_json_params


class EventsView(View):
    @safe_url_params
    def get(self, _request):
        return [EventSerializer(event).data for event in Event.objects.all()]

    @safe_json_params
    def post(self, _request, name: str, date: str):
        event = Event(
            name=name,
            date=dtdate.fromisoformat(date),
            created_at=timezone.now(),
        )

        event.save()

        return EventSerializer(event).data
