from django.contrib.auth.models import User


def user_to_json(u: User):
    return {
        "id": u.id,
        "is_superuser": u.is_superuser,
        "username": u.username,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "is_staff": u.is_staff,
        "is_active": u.is_active,
        "date_joined": u.date_joined,
    }
