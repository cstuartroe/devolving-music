from django.shortcuts import render
from .events import EventViewSet
from .song_submissions import SongSubmissionViewSet


MODEL_ENDPOINTS = {
    "events": EventViewSet,
    "song_submissions": SongSubmissionViewSet,
}


def react_index(request):
    return render(request, 'react_index.html')
