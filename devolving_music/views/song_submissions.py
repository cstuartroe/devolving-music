from rest_framework import viewsets
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer


class SongSubmissionViewSet(viewsets.ModelViewSet):
    queryset = SongSubmission.objects.all()
    serializer_class = SongSubmissionSerializer
