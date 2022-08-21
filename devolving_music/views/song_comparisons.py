from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from rest_framework import permissions
from rest_framework.views import APIView

from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.serializers.song_comparison import SongComparisonSerializer
from .param_utils import success, failure


VOTE_QUOTA_PER_SUB = 10
MAX_VOTE_RATIO = 1.25
EXTRA_VOTES = 200


class SongComparisonsView(LoginRequiredMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SongComparison.objects.all()

    def post(self, request):
        event_id = SongSubmission.objects.get(id=request.data['first_submission_id']).event_id

        # Limit the number of votes based on the number of song submissions

        num_submissions = SongSubmission.objects.filter(event_id=event_id).count()

        votes = SongComparison.objects.filter(
            voter=request.user, created_at__gte=(timezone.now() - timedelta(hours=24))).count()

        if votes >= (num_submissions * VOTE_QUOTA_PER_SUB):
            return failure("Vote quota hit. You may be able to continue voting if more songs are submitted.")

        # Limit the number of votes based on number of others' votes

        votes_by_user = list(
            SongComparison.objects.select_related('first_submission').filter(first_submission__event_id=event_id)
            .values('voter_id').annotate(vcount=Count('id')).order_by('-vcount'))

        print(votes_by_user)

        max_relative_votes = (votes_by_user[1]['vcount']*MAX_VOTE_RATIO + EXTRA_VOTES)

        if (votes_by_user[0]['voter_id'] == request.user.id) and (votes_by_user[0]['vcount'] >= max_relative_votes):
            return failure("You have voted too much relative to others. Please give them a chance to catch up.")

        # Create the SongComparison object

        serializer = SongComparisonSerializer(data={
            **request.data,
            "voter_id": request.user.id,
            "created_at": timezone.now(),
        })

        if not serializer.is_valid():
            return failure(serializer.errors, status=400)

        serializer.save()
        return success(serializer.data)
