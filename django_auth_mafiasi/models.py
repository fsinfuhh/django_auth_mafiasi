import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class MafiasiAuthModelUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=150, unique=True, blank=True)

    REQUIRED_FIELDS = []
