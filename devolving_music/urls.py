from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers, urls as rfurls

from .views import react_index, MODEL_ENDPOINTS
from .views.submit_spotify_playlist import SubmitSpotifyPlaylistView


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
for api_path, viewset in MODEL_ENDPOINTS.items():
    router.register(api_path, viewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/submit_spotify_playlist', SubmitSpotifyPlaylistView.as_view()),
    path('api/', include(router.urls)),
    path('api-auth/', include(rfurls)),
    re_path(r'^.*$', react_index, name="react_index"),
]
