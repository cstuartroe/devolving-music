from django.http import JsonResponse, HttpResponse
from django.db.models import Model
from django.urls import path, re_path
import os
import json


def success(blob):
    return JsonResponse(
        {
            "success": True,
            "result": blob
        },
        status=200
    )


def failure(message: str):
    return JsonResponse(
        {
            "success": False,
            "message": message
        },
        status=400
    )


def resolve_arg_type(t, arg):
    if issubclass(t, Model):
        return t.objects.get(id=int(arg))
    else:
        return t(arg)


def _safe_params(func, params_getter):
    def f(_self, request, **url_params):
        data_params = params_getter(request)

        if len(set(url_params) & set(data_params)) > 0:
            raise ValueError(f"Duplicate param(s): {set(url_params) & set(data_params)}")

        d = {
            **data_params,
            **url_params,
        }

        passed_params = {}
        for argname, t in func.__annotations__.items():
            if argname in d:
                try:
                    passed_params[argname] = resolve_arg_type(t, d[argname])
                except BaseException as e:
                    return failure(str(e))

            else:
                return failure(f"Expected parameter {argname} of type {t}")

        return success(func(_self, request, **passed_params))

    return f


def safe_url_params(func):
    return _safe_params(func, lambda request: request.GET)


def safe_json_params(func):
    return _safe_params(func, lambda request: json.loads(request.body.decode()))


def camelize(snake):
    return "".join(map(str.title, snake.split("_")))


def endpoint_miss(_request):
    return HttpResponse(status=404)


# I need to go take a shower after writing this.
def auto_views():
    view_classes = []

    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and not filename.startswith("_"):
            modname = filename[:-3]
            exec(f"from . import {modname}")
            module = locals()[modname]
            view_class = vars(module)[camelize(modname) + "View"]
            view_classes.append((modname, view_class))

    views = []
    for modname, view_class in view_classes:
        uri = getattr(view_class, "PATH", None) or modname

        views.append(path(uri, view_class.as_view(), name=modname))

    views.append(re_path(r'^.*$', endpoint_miss, name="react_index"))

    return views

