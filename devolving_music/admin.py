from django.contrib import admin
from .models.artist import Artist
from .models.song import Song
from .models.event import Event
from .models.song_submission import SongSubmission
from .models.song_comparison import SongComparison
from .models.duplication_flag import DuplicationFlag

admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Event)
admin.site.register(SongSubmission)
admin.site.register(SongComparison)
admin.site.register(DuplicationFlag)
