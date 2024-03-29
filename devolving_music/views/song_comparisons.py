from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from rest_framework import permissions
from rest_framework.views import APIView

from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.serializers.song_comparison import SongComparisonSerializer
from .param_utils import safe_url_params, success, failure


VOTE_QUOTA_PER_SUB = 10
NUM_CORE_CONTRIBUTORS = 4
MAX_VOTE_RATIO = 2
EXTRA_VOTES_PER_SUB = .5


class SongComparisonsView(LoginRequiredMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SongComparison.objects.all()

    @safe_url_params
    def get(self, _request, event: Event):
        qs = list(SongComparison.objects
                  .select_related('first_submission__song').prefetch_related('first_submission__song__artists')
                  .select_related('first_submission__event').select_related('first_submission__submitter')
                  .select_related('second_submission__song').prefetch_related('second_submission__song__artists')
                  .select_related('second_submission__event').select_related('second_submission__submitter')
                  .select_related('voter')
                  .filter(first_submission__event_id=event.id))

        comparisons = [
            s.to_json()
            for s in qs
        ]

        return success(comparisons)

    def post(self, request):
        event_id = SongSubmission.objects.get(id=request.data['first_submission_id']).event_id
        num_submissions = SongSubmission.objects.filter(event_id=event_id).count()

        # Limit the number of votes based on the number of song submissions

        votes = SongComparison.objects.filter(
            voter=request.user, created_at__gte=(timezone.now() - timedelta(hours=24))).count()

        if votes >= (num_submissions * VOTE_QUOTA_PER_SUB):
            return failure("Vote quota hit. You may be able to continue voting if more songs are submitted.")

        # Limit the number of votes based on number of others' votes

        votes_by_user = list(
            SongComparison.objects.select_related('first_submission').filter(first_submission__event_id=event_id)
            .values('voter_id').annotate(vcount=Count('id')).order_by('-vcount'))

        top_vote_numbers = [v['vcount'] for v in votes_by_user[:NUM_CORE_CONTRIBUTORS]]
        if(len(top_vote_numbers) != 0):
            average_votes = sum(top_vote_numbers)/len(top_vote_numbers)
            max_relative_votes = (average_votes*MAX_VOTE_RATIO) + (num_submissions*EXTRA_VOTES_PER_SUB)
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

        
