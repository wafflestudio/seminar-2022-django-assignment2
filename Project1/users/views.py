from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

from users.models import User, UserFollowing
from users.serializers import CreateUserSerializer, UserSerializer, FollowingSerializer, FollowersSerializer, CreateDestroyFollowingSerializer
from users.permissions import IsSuperUser, IsAccountOwnerOrReadOnly, IsNotLogin

from posts.models import Post
from posts.serializers import PostListSerializer

from comments.models import Comment
from comments.serializers import CommentListCreateSerializer
# Create your views here.
class UserCreateView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsNotLogin]

    def perform_create(self, serializer):
        data = serializer.data
        self.check_object_permissions(self.request, data)
        queryset = User.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already signed up.')
        serializer.save(user=self.request.user)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsSuperUser]
    pagination_class = CursorPagination

    def get_queryset(self):
        try:
            user_list = User.objects.all()
            self.check_object_permissions(self.request, user_list)
            return user_list
        except ObjectDoesNotExist:
            return None


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAccountOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    def get_queryset(self):
        # 노출되어도 되는 정보만 가져올 것
        username = self.kwargs['username']
        if not isinstance(username, str):
            raise ValidationError("username is not correct.")
        user = User.objects.all()
        user = user.filter(username=username)
        if len(user) == 0:
            raise NotFound("There isn't user like that.")
        try:
            self.check_object_permissions(self.request, user)
        except:
            raise PermissionDenied("You're not account owner.")
        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = UserSerializer(instance, context={'request': self.request})
        serializer = self.get_serializer(instance, context={'request':request})
        return Response(serializer.data)

class UserFollowView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateDestroyFollowingSerializer

    def create(self, request, *args, **kwargs):
        following_user_name = self.kwargs['following_user_name']
        following_user = User.objects.filter(username=following_user_name)[0]
        serializer = self.get_serializer(data={**request.data, 'following_user':following_user})

        following_list = UserFollowing.objects.filter(user_id=self.request.user.id)
        if self.request.user == following_user:
            raise ValidationError({'user_id': "You can't follow you."})
        elif following_user in following_list:
            raise ValidationError({'following_user_id': "Already following."})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserUnfollowView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateDestroyFollowingSerializer

class UserFollowingView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.all()
        try:
            self.check_object_permissions(self.request, user)
        except:
            raise PermissionDenied("You don't have permission.")
        userfollowing = UserFollowing.objects.all()
        try:
            queryset = userfollowing.filter(user__username=username)
        except:
            raise NotFound("username is None")
        # 현재 접속한 user 말고 다른 user를 알아오는 방법은 없을까? -> request에서 url을 따오는 방법
        # url의 경우, serializer에 SerializerMethodField로 설정하고 get_field 메소드 정의하여 갖고올 수 있다...
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, context={'request':request})
        return Response(serializer.data)


class UserFollowersView(generics.ListAPIView):
    serializer_class = FollowersSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        if not isinstance(username, str):
            raise ValidationError("username is not correct.")
        user = User.objects.filter(username=username)
        if len(user) == 0:
            raise NotFound("There isn't user like that.")
        user = User.objects.all()
        userfollowing = UserFollowing.objects.all()
        queryset = userfollowing.filter(following_user__username=username)
        try:
            self.check_object_permissions(self.request, user)
        except:
            raise PermissionDenied("You dont't have permission of this method.")
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, context={'request':request})
        return Response(serializer.data)

class UserPostListView(generics.ListAPIView):
    # 앞에 300자만 가져와야 함 + user 정보를 받아서 해당 user의 게시글을 받아와야 함.
    serializer_class = PostListSerializer
    lookup_field = 'username'
    def get_queryset(self):
        username = self.kwargs['username']
        if not isinstance(username, str):
            raise ValidationError("username is not correct.")
        user = User.objects.filter(username=username)
        if len(user) == 0:
            raise NotFound("There isn't user like that.")
        queryset = Post.objects.all()
        queryset = queryset.filter(created_by__username=username)
        try:
            self.check_object_permissions(self.request, queryset)
        except:
            raise PermissionDenied("You don't hane permission of this method.")
        return queryset

class UserCommentListView(generics.ListAPIView):
    serializer_class = CommentListCreateSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        if not isinstance(username, str):
            raise ValidationError("username is not correct.")

        user = User.objects.filter(username=username)
        if len(user) == 0:
            raise NotFound("There isn't user like that.")
        queryset = Comment.objects.all()

        if username is not None:
            queryset = queryset.filter(written_by__username=username)
        else:
            raise ValidationError("username at url is None")

        try:
            self.check_object_permissions(self.request, queryset)
        except:
            raise PermissionDenied("You don't have permission of this method.")
        return queryset

