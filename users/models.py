# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the built-in User model
    to include additional fields.
    """

    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username
