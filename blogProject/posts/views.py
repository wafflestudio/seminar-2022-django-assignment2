from django.shortcuts import render
from rest_framework import generics, request
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer, PostSummarySerializer


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
