from django.contrib.auth.models import User
from rest_framework import mixins, generics, permissions
from django.db.models import Count, F
from rest_framework.permissions import AllowAny

from blog.models import Post, Comment, Tag
from blog.serializers import PostListSerializer, PostSerializer, CommentListSerializer, CommentSerializer, \
    RegisterSerializer
from blog.permissions import IsOwnerOrReadOnly


def delete_unused_tags():
    Tag.objects\
        .annotate(post_count=Count('posts'), comment_count=Count('comments'))\
        .annotate(count_sum=F('post_count')+F('comment_count'))\
        .filter(count_sum=0)\
        .delete()


class PostList(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.model.objects.all()

        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__in=[tag])

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly | permissions.IsAdminUser]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        delete_unused_tags()


class CommentList(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.model.objects.all()

        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__in=[tag])

        post = self.request.GET.get('post')
        if post:
            queryset = queryset.filter(post=post)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly | permissions.IsAdminUser]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        delete_unused_tags()


class UserSignup(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
