from rest_framework import generics, exceptions
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from posts.models import Post, Comment
from posts.permissions import IsAuthorOrReadOnly, IsAuthor
from posts.serializers import PostSerializer, PostSummarySerializer, CommentSerializer


class PostCommentPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'


class PostListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostCommentPagination
    queryset = Post.objects.all()

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
    pagination_class = PostCommentPagination
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
