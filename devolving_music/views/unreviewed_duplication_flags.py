from rest_framework import viewsets
from devolving_music.models.duplication_flag import DuplicationFlag
from devolving_music.models.serializers.duplication_flag import DuplicationFlagSerializer


class UnreviewedDuplicationFlagViewSet(viewsets.ModelViewSet):
    queryset = DuplicationFlag.objects.filter(status__exact='unreviewed')
    serializer_class = DuplicationFlagSerializer
