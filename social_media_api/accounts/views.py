from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User
from django.shortcuts import get_object_or_404
 

from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)
# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(
                user=user
            )

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            token, created = Token.objects.get_or_create(
                user=user
            )

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if request.user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)

        return Response(
            {"message": "User followed successfully."},
            status=status.HTTP_200_OK
        )

class FollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = request.user.following.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class FollowersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = request.user.followers.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class UserFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        users = user.following.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
class UserFollowersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        users = user.followers.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        request.user.following.remove(user_to_unfollow)

        return Response(
            {"message": "User unfollowed successfully."},
            status=status.HTTP_200_OK
        )
       