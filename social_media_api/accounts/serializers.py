from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=6)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_picture",
            "followers",
            "following",
        ]
        read_only_fields = [
            "id",
            "followers",
            "following",
        ]
