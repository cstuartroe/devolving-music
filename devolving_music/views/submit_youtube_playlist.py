import re
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from devolving_music.lib.youtube import get_youtube_playlist_videos
from .param_utils import safe_json_params, success, failure
from devolving_music.models.event import Event
from devolving_music.models.song import Song
from devolving_music.models.artist import Artist
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.lib.song_submission_utils import submit_songs, QuotaExceededError


class SubmitYoutubePlaylistView(LoginRequiredMixin, View):
    PLATFORM = Artist.MusicPlatform.YOUTUBE

    @safe_json_params
    def post(self, request, playlist_link: str, event: Event):
        if not event.allow_youtube:
            return failure(Event.disallowed_platform_message(self.PLATFORM))

        m = re.search(
            r"list=([a-zA-Z\d]+)",
            playlist_link,
        )

        if m is None:
            return failure("Malformed Youtube playlist link. Was it only a link to a single video?")

        playlist_id = m.group(1)

        songs = [
            Song.from_youtube_json(video)
            for video in get_youtube_playlist_videos(playlist_id)
        ]

        try:
            submissions = submit_songs(songs, event=event, submitter=request.user)
            return success([SongSubmissionSerializer(sub).data for sub in submissions])
        except QuotaExceededError as e:
            return failure(str(e))
