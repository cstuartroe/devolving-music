from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers, urls as rfurls

from .views import react_index
from .views.events import EventViewSet
from .views.submit_spotify_playlist import SubmitSpotifyPlaylistView
from .views.submit_youtube_playlist import SubmitYoutubePlaylistView
from .views.song_comparisons import SongComparisonsView
from .views.get_song_pair import GetSongPairView
<<<<<<< HEAD
from .views.unreviewed_duplication_flags import UnreviewedDuplicationFlagViewSet
from .views.printView import printMe
=======
from .views.unreviewed_duplication_flags import UnreviewedDuplicationFlagView

>>>>>>> b5cd353e13645f796fb8b2260db08f616f02548a

class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register('events', EventViewSet)

urlpatterns = [
    re_path('admin/?', admin.site.urls),
    path('api/submit-playlist/Spotify', SubmitSpotifyPlaylistView.as_view()),
    path('api/submit-playlist/YouTube', SubmitYoutubePlaylistView.as_view()),
    path('api/pair', GetSongPairView.as_view()),
    path('api/song_comparisons', SongComparisonsView.as_view()),
    path('api/unreviewed_duplication_flags', UnreviewedDuplicationFlagView.as_view()),
    path('api/', include(router.urls)),
    path('api-auth/', include(rfurls)),
    path('print',printMe),
    re_path(r'^.*$', react_index, name="react_index"),
]
