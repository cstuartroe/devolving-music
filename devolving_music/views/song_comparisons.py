from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView
from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.serializers.song_comparison import SongComparisonSerializer
from .param_utils import success, failure


class SongComparisonsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SongComparison.objects.all()

    def post(self, request):
        serializer = SongComparisonSerializer(data={
            **request.data,
            "created_at": timezone.now(),
        })

        if not serializer.is_valid():
            return failure(serializer.errors, status=400)

        serializer.save()
        return success(serializer.data)
