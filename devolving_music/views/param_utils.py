from django.http import JsonResponse
from django.db.models import Model
import json


def success(blob):
    return JsonResponse(
        {
            "success": True,
            "result": blob
        },
        status=200
    )


def failure(message: str, status: int = 400):
    return JsonResponse(
        {
            "success": False,
            "message": message
        },
        status=status
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

        return func(_self, request, **passed_params)

    return f


def safe_url_params(func):
    return _safe_params(func, lambda request: request.GET)


def safe_json_params(func):
    return _safe_params(func, lambda request: json.loads(request.body.decode()))
