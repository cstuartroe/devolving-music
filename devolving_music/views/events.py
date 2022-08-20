from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets

from devolving_music.models.event import Event
from devolving_music.models.serializers.event import EventSerializer


class EventViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Event.objects.filter(visible__exact=True)
    serializer_class = EventSerializer
