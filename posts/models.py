from django.db import models
from users.models import CustomUser as User


class Post(models.Model):
    """
    A Post made by a user. This includes text, images, videos, and more.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    video = models.FileField(upload_to="post_videos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(
        max_length=10,
        choices=[("public", "Public"), ("private", "Private")],
        default="public",
    )

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"
