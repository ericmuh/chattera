from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # List all posts
    path("", PostListView.as_view(), name="post_list"),
    # Create a new post
    path("create/", PostCreateView.as_view(), name="post_create"),
    # Retrieve a specific post by ID
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    # Update a specific post by ID
    path("<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    # Delete a specific post by ID
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
]
