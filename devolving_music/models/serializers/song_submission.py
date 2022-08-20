from django.contrib.auth.models import User
from rest_framework import serializers
from devolving_music.models.song_submission import SongSubmission


class SongSubmissionSerializer(serializers.ModelSerializer):
    submitted_id = serializers.PrimaryKeyRelatedField(
        source='submitter',
        queryset=User.objects.all(),
    )

    class Meta:
        model = SongSubmission
        fields = "__all__"
        depth = 2
