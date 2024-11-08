from django.urls import path
from .views import (
    LikePostView,
    CommentPostView,
)

urlpatterns = [
    # Like a post (or remove like)
    path("like/<int:post_id>/", LikePostView.as_view(), name="like_post"),
    # Comment on a post
    path("comment/<int:post_id>/", CommentPostView.as_view(), name="comment_post"),
]
