from django.db import models
from users.models import CustomUser as User
from posts.models import Post  # Import Post model from the posts app


class Like(models.Model):
    """
    Like functionality for posts.
    """

    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "post",
            "user",
        )
        # Prevents duplicate likes from the same user on the same post

    def __str__(self):
        return f"Like by {self.user.username} on Post {self.post.id}"


class Comment(models.Model):
    """
    Comment functionality for posts.
    """

    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the comment was made
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )  # Allows replies to comments

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"


class Share(models.Model):
    """
    Share functionality for posts.
    """

    post = models.ForeignKey(Post, related_name="shares", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="shares", on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the post was shared

    def __str__(self):
        return f"Share by {self.user.username} on Post {self.post.id}"


# class PostReport(models.Model):
#     """
#     Report a post for inappropriate content or violations.
#     """

#     post = models.ForeignKey(Post, related_name="reports", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name="reports", on_delete=models.CASCADE)
#     reason = models.CharField(max_length=255)  # Reason for reporting the post
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )  # Timestamp when the report was made

#     def __str__(self):
#         return f"Report on Post {self.post.id} by {self.user.username}"
