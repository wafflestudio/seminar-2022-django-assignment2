from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, request, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from posts.models import Post, Comment
from posts.permissions import IsAuthorOrReadOnly, IsAuthor
from posts.serializers import PostSerializer, PostSummarySerializer, CommentSerializer


class PostListView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    # serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostSerializer
        return PostSummarySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.kwargs['pk']
        return queryset.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(post_id=post_id, author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor | IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed("GET")

    def perform_update(self, serializer):
        post_id = self.kwargs['ppk']
        serializer.save(post_id=post_id, is_updated=True)
