# posts/serializers.py
from rest_framework import serializers
from .models import Post
from users.models import CustomUser as User


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing posts.
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )  # Represent the user as an ID

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "image",
            "video",
            "created_at",
            "updated_at",
            "visibility",
            "is_active",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of a post (includes comments, likes, etc).
    """

    user = serializers.StringRelatedField()  # User's username as a string
    comments = serializers.StringRelatedField(many=True)  # Comments related to the post
    likes_count = serializers.IntegerField(
        source="likes.count", read_only=True
    )  # Number of likes for the post
    shares_count = serializers.IntegerField(
        source="shares.count", read_only=True
    )  # Number of shares for the post

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "image",
            "video",
            "created_at",
            "updated_at",
            "visibility",
            "is_active",
            "comments",
            "likes_count",
            "shares_count",
        ]
