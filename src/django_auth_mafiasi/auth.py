from collections import defaultdict
from typing import *
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import MafiasiAuthModelUser


def _is_in_groups(token: dict, required_groups: List[str]) -> bool:
    if "*" in required_groups:
        return True
    if token["groups"] == "":
        return False

    return required_groups == [i for i in required_groups if i in token["groups"]]


def get_user_from_token(id_token: dict):
    id_token = defaultdict(lambda: "", **id_token)

    User = get_user_model()
    user: MafiasiAuthModelUser
    user, created = User.objects.get_or_create(id=id_token["sub"])

    user.username = id_token["username"]
    user.first_name = id_token["given_name"]
    user.last_name = id_token["family_name"]
    user.email = id_token["email"]
    user.is_staff = _is_in_groups(id_token, settings.AUTH_STAFF_GROUPS)
    user.is_superuser = _is_in_groups(id_token, settings.AUTH_SUPERUSER_GROUPS)

    user.set_unusable_password()
    user.clean_fields()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.save()

    return user
