from rest_framework import serializers
from devolving_music.models.event import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
