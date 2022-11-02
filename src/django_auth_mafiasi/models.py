import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


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
        return f"{self.id} ({self.username if self.username else 'unknown'})"
