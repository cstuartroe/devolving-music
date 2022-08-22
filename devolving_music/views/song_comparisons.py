from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from rest_framework.views import APIView

from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.serializers.song_comparison import SongComparisonSerializer
from .param_utils import success, failure


DAILY_VOTE_QUOTA = 200


class SongComparisonsView(LoginRequiredMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SongComparison.objects.all()

    def post(self, request):
        already_voted_today = SongComparison.objects.filter(
            voter=request.user,
            created_at__gte=(datetime.utcnow() - timedelta(hours=24)),
        )

        if len(list(already_voted_today)) > DAILY_VOTE_QUOTA:
            return failure("Vote quota hit for the day.")

        serializer = SongComparisonSerializer(data={
            **request.data,
            "voter_id": request.user.id,
            "created_at": timezone.now(),
        })

        if not serializer.is_valid():
            return failure(serializer.errors, status=400)

        serializer.save()
        return success(serializer.data)
