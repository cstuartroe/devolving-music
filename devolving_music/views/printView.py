from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import render_to_string

from django.views import View
from .param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer

def printMe(request,Value="Hello Buddy"):
    #updates page is the home page
    voteable_submissions = [
            sub
            for sub in SongSubmission.objects.filter(event__exact=1).order_by('?')
            if sub.voteable()
        ]
    sub1= voteable_submissions[:]
    Value=sub1
    return render(request,"index_test.html",{'content':Value})