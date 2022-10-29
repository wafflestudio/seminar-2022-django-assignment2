from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostListSerializer, PostDetailSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly|IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer


