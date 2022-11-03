from typing import *

from django.contrib.auth import get_user_model
from django.apps import AppConfig
from django.core.checks import register, CheckMessage, Warning
from oic.oic import Client

from django_auth_mafiasi import auth_utils


class DjangoAuthMafiasiConfig(AppConfig):
    name = "django_auth_mafiasi"
    oic_client: Client

    def ready(self):
        super().ready()
        self.oic_client = auth_utils.create_client()


@register
def check_user_model(app_configs, **kwargs) -> List[CheckMessage]:
    from .models import MafiasiAuthModelUser

    if not issubclass(get_user_model(), (MafiasiAuthModelUser,)):
        return [
            Warning(
                "The user model might not be compatible with Mafiasi authentication",
                hint="Set AUTH_USER_MODEL to django_auth_mafiasi.MafiasiAuthModelUser or a derived class",
                obj=get_user_model(),
                id=f"{DjangoAuthMafiasiConfig.name}:W001",
            )
        ]
    return []
