from collections import defaultdict
from typing import *
from django.contrib.auth import get_user_model
from django.conf import settings
from oic.oic import Client, RegistrationResponse
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

if TYPE_CHECKING:
    from .models import MafiasiAuthModelUser


def is_in_groups(token: dict, required_groups: List[str]) -> bool:
    """
    Check whether the given encoded token is in one of the given required groups.

    This is used to verify if a user is in one of the configured *AUTH_STAFF_GROUPS* or *AUTH_SUPERUSER_GROUPS*
    """
    if "*" in required_groups:
        return True
    if "groups" not in token.keys() or token["groups"] is None:
        return False

    return [g for g in required_groups if g in token["groups"]] == required_groups


def get_client():
    """
    Construct an appropriately configured OpenId Connect client instance
    """
    client = Client(
        client_id=settings.AUTH_CLIENT_ID, client_authn_method=CLIENT_AUTHN_METHOD
    )
    client.provider_config(issuer=settings.AUTH_SERVER)
    client.store_registration_info(
        RegistrationResponse(
            client_id=settings.AUTH_CLIENT_ID, client_secret=settings.AUTH_CLIENT_SECRET
        )
    )

    return client


def get_user_from_access_token(token: dict):
    """
    Get a user object from the given access token, creating one if no such user already exists.

    Access tokens are designed to provide access to an application.
    They therefore only contain the bare minimum information to identify a user as well as cryptographic material to substantiate that claim.
    """
    User = get_user_model()
    user, created = User.objects.get_or_create(id=token["sub"])
    return user


def get_user_from_id_token(id_token: dict):
    """
    Get a user object from the given id token, creating one if no such user already exists.

    ID tokens are designed to identify a user and might contain much information about the user.
    Therefore, this function extracts as much information as possible from the ID token and automatically updates the user object accordingly.
    """
    User = get_user_model()  # type: Type[MafiasiAuthModelUser]
    user, _ = User.objects.get_or_create(id=id_token["sub"])
    user.update_from_token(id_token)
    user.full_clean()
    user.save()
    return user
