from django.core.management.base import BaseCommand


from math import nan
from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import render_to_string

from django.views import View
from devolving_music.views.param_utils import safe_url_params, success, failure
from devolving_music.lib.song_utils import get_song_color
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.models.song_comparison import SongComparison
from devolving_music.models.song import Song
from devolving_music.lib.get_scores import *
import pdb 
#use for debugging
# pdb.set_trace()
cached_submissions=SongSubmission.get_voteable_submissions(3)
energy_submissions=[]
Comparison_submissions = SongComparison.get_event_comparisons(3)
Song1=Comparison_submissions[0].first_submission
Song2=Comparison_submissions[0].second_submission 
SongSubmission.get_scores(Comparison_submissions)
for Song in cached_submissions:
    energy_submissions.append(Song.energy_score)

def printMe(request,Value="Hello Buddy"):
    #updates page is the home page
    
    Song3=SongSubmission.objects.get(id=395)
    #get_scores(Comparison_submissions)
    SongSubmission.get_scores(Comparison_submissions)
    i=0
    # for Song in cached_submissions:
    #     energy_submissions[i]=Song
    #     i=i+1
    return render(request,"index_test.html",{'content': cached_submissions[-2].energy_score,'content2':Song1.energy_score})
