import uuid
from collections import defaultdict
from collections.abc import Mapping

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from oic.oauth2 import ErrorResponse

from django_auth_mafiasi import auth_utils


# TODO Add Group model and add links to groups into appropriate mixins


class MafiasiAuthModelUser(AbstractUser):
    """
    The base Mafiasi user model from which all other user models should be extended.

    It provides an id field that is compatible with mafiasi-identity IDs as well as additional fields that might
    be empty depending on whether the django app requests the relevant scopes from mafiasi-identity.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # the username field is always null if unset to avoid uniqueness errors
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email_verified = models.BooleanField(null=True, blank=True)
    display_name = models.CharField(max_length=150, blank=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.id} ({self.username if self.username else 'username unknown'})"

    def update_from_token(self, token: Mapping[str, str]):
        """
        Update user data from a supplied token.
        This token could be an access token, id token or even a userinfo response object.

        !! This does not save the model back to DB but only makes changes to the current instance !!
        """
        token = defaultdict(lambda: None, **token)

        # we set username to None instead of a blank string to avoid unique constraint collisions
        self.username = token["username"]
        self.first_name = token["given_name"] or ""
        self.last_name = token["family_name"] or ""
        self.display_name = token["display_name"] or ""
        self.email = token["email"] or ""
        self.email_verified = token["email_verified"]
        self.is_staff = auth_utils.is_in_groups(token, settings.AUTH_STAFF_GROUPS)
        self.is_superuser = auth_utils.is_in_groups(
            token, settings.AUTH_SUPERUSER_GROUPS
        )

        if self.password == "":
            self.set_unusable_password()

    def refresh_from_mafiasi_identity(self):
        """
        Try to refresh user data from mafiasi-identity.

        !! This does not save the model back to DB but only makes changes to the current instance !!

        :raises RuntimeError: if it was not possible to refresh the user data either because there are no valid
        tokens or some other internal error
        """
        try:
            self.tokens
        except UserToken.DoesNotExist as e:
            raise RuntimeError(f"There are no tokens for user {self}") from e

        client = auth_utils.get_client()
        response = client.do_user_info_request(
            scope=settings.AUTH_SCOPE,
            token=self.tokens.access_token,
        )
        if isinstance(response, ErrorResponse):
            raise RuntimeError(
                f"Could not request userinfo using access token", response.to_dict()
            )

        self.update_from_token(response)


class UserToken(models.Model):
    """
    A model which stores mafiasi-identity authentication tokens for a user object
    """

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="tokens",
    )
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
