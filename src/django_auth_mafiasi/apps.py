from typing import *

from django.contrib.auth import get_user_model
from django.apps import AppConfig
from django.core.checks import register, CheckMessage, Warning


class MafiasiAuthConfig(AppConfig):
    name = "django_auth_mafiasi"


@register
def check_user_model(app_configs, **kwargs) -> List[CheckMessage]:
    from .models import MafiasiAuthModelUser

    if not issubclass(get_user_model(), (MafiasiAuthModelUser,)):
        return [
            Warning(
                "The user model might not be compatible with Mafiasi authentication",
                hint="Set AUTH_USER_MODEL to django_auth_mafiasi.MafiasiAuthModelUser or a derived class",
                obj=get_user_model(),
                id=f"{MafiasiAuthConfig.name}:W001",
            )
        ]
    return []
