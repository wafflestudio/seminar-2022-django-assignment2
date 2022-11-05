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

    # def get(self, request, *args, **kwargs):
    #     print(request.user)
    #     return super().get(self, request, *args, **kwargs)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor | IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed("GET")

# class CommentUpdateView(generics.UpdateAPIView):
#     permission_classes = [IsAuthor]
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#
# class CommentDestroyView(generics.DestroyAPIView):
#     permission_classes = [IsAuthor]
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
