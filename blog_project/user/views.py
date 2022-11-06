from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from post.models import Post, Comment, Tag, Clapse
from .serializers import UserSerializer
from .permissions import IsAuthorOrReadOnly
from notification import views as notification_views
import time


class RegisterUser(generics.CreateAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):

    permission_classes = ()

    def post(self, request, ):

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class FollowUser(APIView):

    permission_classes = ()

    def post(self, request, pk, format=None):
        user = request.user
        user_following = user.following.all()

        try:
            user_to_follow = User.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user_to_follow in user_following:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        else:
            user.following.add(user_to_follow)
            user_to_follow.followers.add(user)
            notification_views.create_notification(
                user, user_to_follow, 'follow')
            return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    permission_classes = ()

    def post(self, request, pk, format=None):
        user = request.user
        following = user.following.all()

        try:
            user_to_unfollow = User.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow not in following:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        else:
            user.following.remove(user_to_unfollow)
            user_to_unfollow.followers.remove(user)

            notification_views.create_notification(
                user, user_to_unfollow, 'unfollow')

            return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    permission_classes = ()

    def get(self, request, format=None):

        user = request.user
        found_user = User.objects.get(pk=user.pk)
        if (found_user is None):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(
            found_user, context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
