from django.contrib.auth.models import User
from rest_framework import serializers
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison


class SongComparisonSerializer(serializers.ModelSerializer):
    first_submission_id = serializers.PrimaryKeyRelatedField(
        source='first_submission',
        queryset=SongSubmission.objects.all(),
    )
    second_submission_id = serializers.PrimaryKeyRelatedField(
        source='second_submission',
        queryset=SongSubmission.objects.all(),
    )
    voter_id = serializers.PrimaryKeyRelatedField(
        source='voter',
        queryset=User.objects.all(),
    )

    class Meta:
        model = SongComparison
        fields = "__all__"
        depth = 2
