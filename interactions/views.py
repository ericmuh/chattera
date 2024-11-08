# interactions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Like, Comment
from rest_framework.permissions import IsAuthenticated
from .serializers import LikeSerializer, ShareSerializer, CommentSerializer
from posts.models import Post
from posts.serializers import PostSerializer


class LikePostView(APIView):
    """
    Like or unlike a post.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Allows a user to like or unlike a post by providing the post's ID.
        If the user has already liked the post, it will be unliked. If not, the post will be liked.
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()  # If the like already exists, delete it (unlike the post)
            return Response({"status": "unliked"}, status=status.HTTP_200_OK)

        return Response({"status": "liked"}, status=status.HTTP_200_OK)


class SharePostView(APIView):
    """
    Share a post by creating a new post that is associated with the original one.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Allows a user to share a post. The shared post will be linked to the original post.
        A new post is created, and the user becomes the author of the shared post.
        """
        try:
            post_to_share = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        # Create a new post with the same content but authored by the user who is sharing
        shared_post = Post.objects.create(
            title=f"Shared: {post_to_share.title}",
            content=post_to_share.content,
            author=user,  # The user sharing the post becomes the author
        )

        return Response(
            PostSerializer(shared_post).data, status=status.HTTP_201_CREATED
        )


class CommentPostView(APIView):
    """
    Comment on a post.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Allows a user to comment on a post by providing the post's ID and comment content.
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        comment_content = request.data.get("content")
        parent_comment_id = request.data.get("parent", None)

        # Check if the parent comment exists, if it's a reply
        parent_comment = None
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            except Comment.DoesNotExist:
                return Response(
                    {"detail": "Parent comment not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Create a new comment linked to the post and optionally to a parent comment
        comment = Comment.objects.create(
            post=post, user=user, content=comment_content, parent=parent_comment
        )

        # Serialize the new comment
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


# class FriendRequestView(APIView):
#     """
#     Send a friend request to another user
#     """

#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         user_to = User.objects.get(id=user_id)
#         user_from = request.user

#         # Prevent sending request to self
#         if user_from == user_to:
#             return Response(
#                 {"detail": "Cannot send a friend request to yourself."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Create a new friend request
#         friend_request = FriendRequest.objects.create(
#             from_user=user_from, to_user=user_to
#         )
#         return Response(
#             FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED
#         )


# class AcceptFriendRequestView(APIView):
#     """
#     Accept a pending friend request
#     """

#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         user_to = request.user
#         user_from = User.objects.get(id=user_id)

#         # Check if a friend request exists
#         try:
#             friend_request = FriendRequest.objects.get(
#                 from_user=user_from, to_user=user_to
#             )
#             friend_request.accepted = True
#             friend_request.save()
#             return Response(
#                 {"status": "Friend request accepted"}, status=status.HTTP_200_OK
#             )
#         except FriendRequest.DoesNotExist:
#             return Response(
#                 {"detail": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND
#             )
