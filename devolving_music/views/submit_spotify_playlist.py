import re
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from devolving_music.lib.spotify import get_song_data
from .param_utils import safe_json_params, success, failure
from devolving_music.models.event import Event
from devolving_music.models.song import Song
from devolving_music.models.artist import Artist
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.lib.song_submission_utils import submit_songs, QuotaExceededError


class SubmitSpotifyPlaylistView(LoginRequiredMixin, View):
    PLATFORM = Artist.MusicPlatform.SPOTIFY

    @safe_json_params
    def post(self, request, playlist_link: str, event: Event):
        if not event.allow_spotify:
            return failure(Event.disallowed_platform_message(self.PLATFORM))

        m = re.match(
            r"^https://open.spotify.com/playlist/([a-zA-Z\d]+)",
            playlist_link,
        )

        if m is None:
            return failure("Malformed Spotify link.")

        playlist_id = m.group(1)

        tracks = [
            Song.from_spotify_json(track)
            for track in get_song_data(playlist_id)
            if not track["is_local"]
        ]

        try:
            submissions = submit_songs(tracks, event=event, submitter=request.user)
            return success([SongSubmissionSerializer(sub).data for sub in submissions])
        except QuotaExceededError as e:
            return failure(str(e))
        except BaseException as e:
            return failure(str(e), status=500)
