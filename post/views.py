from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import Post, Comment, Tag
from .serializers import PostDetailSerializer, PostListSerializer, CommentSerializer, TagPostSerializer, TagCommentSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import PostPagination, CommentPagination, TagPagination
import ast
import json

# Create your views here.


class UserCreate(generics.CreateAPIView):
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


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_class = (IsAuthorOrReadOnly, )
    pagination_class = PostPagination

    def post(self, request, *args, **kwargs):
        created_by = request.user
        summary_for_list_api = request.data["description"][:300]
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=created_by,
                            summary_for_list_api=summary_for_list_api)
            print(serializer.data)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_class = (IsAuthorOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CommentList(generics.ListCreateAPIView):
    permission_class = (IsAuthorOrReadOnly, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def post(self, request, *args, **kwargs):
        created_by = request.user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=created_by)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_class = (IsAuthorOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TagPostList(generics.ListCreateAPIView):
    permission_class = (IsAuthorOrReadOnly, )
    queryset = Tag.objects.all()
    serializer_class = TagPostSerializer
    pagination_class = TagPagination

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagCommentList(generics.ListCreateAPIView):
    permission_class = (IsAuthorOrReadOnly, )
    queryset = Tag.objects.all()
    serializer_class = TagCommentSerializer
    pagination_class = TagPagination

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
