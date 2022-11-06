from django.contrib.auth.models import User
from django.db.models import Count, F
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

from blog.models import Post, Comment, Tag, UserFollowing
from blog.permissions import IsOwnerOrReadOnly, IsObjectOwnerOrReadOnly
from blog.serializers import PostListSerializer, PostSerializer, CommentSerializer, RegisterSerializer, \
    UserFollowingSerializer


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
    permission_classes = [IsObjectOwnerOrReadOnly | permissions.IsAdminUser]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        delete_unused_tags()


class CommentList(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
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
    permission_classes = [IsObjectOwnerOrReadOnly | permissions.IsAdminUser]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        delete_unused_tags()


class UserFollowingList(generics.ListCreateAPIView):
    model = UserFollowing
    serializer_class = UserFollowingSerializer
    permission_classes = [IsOwnerOrReadOnly | permissions.IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        return user.following.all()

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return HttpResponseBadRequest(e)
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserFollowersList(generics.ListAPIView):
    serializer_class = UserFollowingSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        return user.followers.all()


class UserFollowingDestroy(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly | permissions.IsAdminUser]
    serializer_class = UserFollowingSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']
        return get_object_or_404(UserFollowing, user=pk, following_user=other_pk)


class UserSignup(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
