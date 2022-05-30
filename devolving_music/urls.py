from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers, urls as rfurls

from .views import react_index
from .views.events import EventViewSet
from .views.song_submissions import SongSubmissionViewSet
from .views.submit_spotify_playlist import SubmitSpotifyPlaylistView


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register('events', EventViewSet)
router.register('song_submissions', SongSubmissionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/submit_spotify_playlist', SubmitSpotifyPlaylistView.as_view()),
    path('api/', include(router.urls)),
    path('api-auth/', include(rfurls)),
    re_path(r'^.*$', react_index, name="react_index"),
]
