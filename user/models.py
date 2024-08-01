import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


def avatar_image_file_path(instance: "User", filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/avatars/", filename)


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to=avatar_image_file_path, null=True, blank=True
    )

    def __str__(self):
        return self.username
