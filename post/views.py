from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Tag
from .serializers import PostDetailSerialzier, PostListSerializer, CommentSerializer, TagPostSerializer, TagCommentSerializer, UserSerializer

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
    ordering_fields = ['created_at']


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerialzier
    # 필요한 경우
    # permission_class = (IsAuthorOrReadOnly, )
    # 집어넣기


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TagPostList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagPostSerializer


class TagCommentList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagCommentSerializer
