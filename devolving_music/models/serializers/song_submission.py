from rest_framework import serializers
from devolving_music.models.song_submission import SongSubmission


class SongSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongSubmission
        fields = "__all__"
        depth = 2
