from django.core.management.base import BaseCommand
from django.db.models.fields import BigAutoField, CharField, DateField, DateTimeField, BooleanField
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from django.contrib.auth.models import User

from devolving_music.models.artist import Artist
from devolving_music.models.song import Song
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.duplication_flag import DuplicationFlag


class Command(BaseCommand):
    help = 'Export the current playlist to Spotify'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass

