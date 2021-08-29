from django.shortcuts import render
from ._utils import auto_views


def react_index(request):
    return render(request, 'react_index.html')
