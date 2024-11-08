# interactions/serializers.py
from rest_framework import serializers
from .models import Like, Share, Comment
from posts.models import Post
from users.models import CustomUser as User


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for liking a post.
    """

    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = [
            "created_at"
        ]  # Do not allow direct modification of 'created_at'


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing comments on posts.
    """

    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )  # Link to the post
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )  # User who made the comment
    parent = serializers.PrimaryKeyRelatedField(
        queryset="self", required=False, allow_null=True
    )  # Allow replies to comments

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "content", "created_at", "updated_at", "parent"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_content(self, value):
        """
        Ensure that the comment content is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value


class ShareSerializer(serializers.ModelSerializer):
    """
    Serializer for sharing a post.
    """

    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Share
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["created_at"]  # 'created_at' should be automatically set
