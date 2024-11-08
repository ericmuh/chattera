from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.views import APIView
from .models import CustomUser


class UserProfileView(APIView):
    """
    View and update the authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the user profile (viewing own profile)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # Update the user profile (bio, phone number, etc.)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    """
    Handle user registration.
    """

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handle user login and return a JWT token.
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserListView(APIView):
    """
    List all users (admin only).
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserUpdateView(APIView):
    """
    Update user details (admin only).
    """

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
