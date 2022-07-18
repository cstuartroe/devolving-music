import re
from django.views import View
from devolving_music.lib.youtube import get_youtube_playlist_videos
from .param_utils import safe_json_params, success, failure
from devolving_music.models.event import Event
from devolving_music.models.song import Song
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.lib.song_submission_utils import submit_song


class SubmitYoutubePlaylistView(View):
    @safe_json_params
    def post(self, _request, playlist_link: str, event: Event):
        m = re.search(
            r"list=([a-zA-Z\d]+)",
            playlist_link,
        )

        if m is None:
            return failure("Malformed Youtube playlist link. Was it only a link to a single video?")

        playlist_id = m.group(1)

        video_data = get_youtube_playlist_videos(playlist_id)

        submissions = []
        for video in video_data:
            song = Song.from_youtube_json(video)
            sub = submit_song(song=song, event=event)
            submissions.append(sub)

        return success([SongSubmissionSerializer(sub).data for sub in submissions])
