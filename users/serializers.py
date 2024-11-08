# users/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user with additional fields like bio, profile picture, etc.
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "bio",
            "profile_picture",
            "phone_number",
            "gender",
        ]

    def validate(self, data):
        """
        Validate that password and password2 match.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        """
        Create and return the user.
        """
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture", ""),
            phone_number=validated_data.get("phone_number", ""),
            gender=validated_data.get("gender", ""),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user details.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
            "phone_number",
            "gender",
        ]
