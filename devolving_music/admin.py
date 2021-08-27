from django.contrib import admin
from .models import *

admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Event)
admin.site.register(SongSubmission)
admin.site.register(SongComparison)
