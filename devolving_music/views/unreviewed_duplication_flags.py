from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions
from rest_framework.views import APIView

from devolving_music.models.duplication_flag import DuplicationFlag
from devolving_music.models.serializers.duplication_flag import DuplicationFlagSerializer
from .param_utils import success, failure


class UnreviewedDuplicationFlagView(LoginRequiredMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return DuplicationFlag.objects.filter(status__exact='unreviewed')

    def get(self, _request):
        serializer = DuplicationFlagSerializer(self.get_queryset(), many=True)
        return success(serializer.data)

    # This isn't really good RESTful semantics - this POST endpoint is used *only* for updating!
    def post(self, request):
        serializer = DuplicationFlagSerializer(
            DuplicationFlag.objects.get(id=request.data["id"]),
            data={
                "status": request.data["status"],
                "reviewed_at": timezone.now(),
            },
        )

        if not serializer.is_valid():
            return failure(serializer.errors, status=400)

        serializer.save()
        return success(serializer.data)
