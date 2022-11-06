from rest_framework import generics
import rest_framework.permissions as permission_set
from rest_framework.pagination import CursorPagination

from blog.models import Post, Comment, Tag
from .permissions import IsAdminOrCreatorOrReadOnly
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer, CommentDetailSerializer, \
    TagSerializer


class PostPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 10


class CommentPagination(CursorPagination):
    ordering = 'created_at'
    page_size = 10


class TagPagination(CursorPagination):
    ordering = 'content'
    page_size = 10


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permission_set.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'pid'
    permission_classes = [IsAdminOrCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CommentView(generics.ListCreateAPIView):
    permission_classes = [permission_set.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pid'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # comment의 post에 to_internal_value로 값을 설정해주기 위해 context에 post 값 전달
        context['post'] = self.kwargs['pid']
        return context


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'cid'
    permission_classes = [IsAdminOrCreatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class TagListViewOnly(generics.ListAPIView):
    permission_classes = [permission_set.AllowAny]
    pagination_class = TagPagination
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
