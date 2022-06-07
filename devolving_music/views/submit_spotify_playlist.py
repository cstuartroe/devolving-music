import re
from django.views import View
from devolving_music.lib.spotify import get_song_data
from .param_utils import safe_json_params, success, failure
from devolving_music.models.event import Event
from devolving_music.models.song import Song
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.lib.song_submission_utils import submit_song


class SubmitSpotifyPlaylistView(View):
    @safe_json_params
    def post(self, _request, playlist_link: str, event: Event):
        m = re.match(
            r"^https://open.spotify.com/playlist/([a-zA-Z\d]+)",
            playlist_link,
        )

        if m is None:
            return failure("Malformed Spotify link.")

        playlist_id = m.group(1)

        submissions = []
        for track in get_song_data(playlist_id):
            if not track["is_local"]:
                song = Song.from_spotify_json(track)
                sub = submit_song(song=song, event=event)
                submissions.append(sub)

        return success([SongSubmissionSerializer(sub).data for sub in submissions])
