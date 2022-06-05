from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.serializers.song_comparison import SongComparisonSerializer


class SongComparisonsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SongComparison.objects.all()

    def get(self, _request):
        serializer = SongComparisonSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SongComparisonSerializer(data={
            **request.data,
            "created_at": timezone.now(),
        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response(serializer.data, status=201)
