from django.core.management.base import BaseCommand

from devolving_music.lib.song_scores import SongScores
from devolving_music.lib.spotify import add_songs
from devolving_music.models.event import Event


class Command(BaseCommand):
    help = 'Export the current playlist for a given event to Spotify'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)

    def handle(self, *args, event_id, **options):
        event = Event.objects.get(pk=event_id)
        scores = SongScores.all_from_event(event).get_final_list()
        song_ids = [
            score.song_submission.song.platform_id
            for score in scores.scores_list
            if score.song_submission.song.artists.all()[0].platform == "Spotify"
        ]
        add_songs(event.spotify_playlist_id, song_ids)


