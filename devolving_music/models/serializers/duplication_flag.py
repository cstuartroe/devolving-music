from rest_framework import serializers
from devolving_music.models.duplication_flag import DuplicationFlag


class DuplicationFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuplicationFlag
        fields = "__all__"
        depth = 3
