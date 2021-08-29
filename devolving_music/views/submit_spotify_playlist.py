from django.views import View
from devolving_music.lib.spotify import spotify_client
from ._utils import safe_json_params
from devolving_music.models import Event, Song, SongSubmission
from devolving_music.models.serializers import SongSubmissionSerializer
import re


class SubmitSpotifyPlaylistView(View):
    @safe_json_params
    def post(self, _request, playlist_link: str, event: Event):
        tracks = []
        offset = 0

        m = re.match(
            r"^https://open.spotify.com/playlist/([a-zA-Z0-9]+)",
            playlist_link,
        )
        playlist_id = m.group(1)

        while True:
            res = spotify_client.playlist_tracks(
                playlist_id=playlist_id,
                fields="items(track(id, name, artists(id, name), is_local))",
                limit=100,
                offset=offset
            )

            if len(res["items"]) == 0:
                break

            tracks += res["items"]
            offset += 100

        submissions = []
        for track in tracks:
            if not track["track"]["is_local"]:
                song = Song.from_spotify_json(track)
                submissions.append(SongSubmission.submit(song=song, event=event))

        return [SongSubmissionSerializer(sub).data for sub in submissions]
