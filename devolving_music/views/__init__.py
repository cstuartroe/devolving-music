from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout


def react_index(request):
    if not request.user.is_active:
        r = HttpResponseRedirect("/admin/login/?next=/")
        return r

    return render(request, 'react_index.html', {"user_email": request.user.email})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")
