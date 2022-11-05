from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.response import Response

from .permissions import IsCreatorOrReadOnly
from .models import Post, TagToPost

from posts.serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer
# Create your views here.
class StandardCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = 'id'
    ordering = '-created_at'
class PostListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = StandardCursorPagination

class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer

    # def perform_create(self, serializer):
    #     TagToPost.save()
    #     serializer.save()

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # model에서 참조하는 필드명인 듯?
    lookup_field = 'id'
    # url에서 갖고 오는 parameter명
    lookup_url_kwarg = 'post_id'

    # def perform_update(self, serializer):
    #

    def get_queryset(self):
        posts = Post.objects.all()
        return posts

    def get_object(self):
        post_id = self.kwargs['post_id']
        posts = self.get_queryset()
        post = posts.filter(id=post_id)
        post = get_object_or_404(post)
        if post is None:
            raise NotFound("There is no post like that.")
        try:
            self.check_object_permissions(self.request, post)
        except:
            raise PermissionDenied("You're not creator of this post.")
        return post

class PostListByTagView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'content'
    lookup_url_kwarg = 'content'

    def get_queryset(self):
        tag_content = self.kwargs['content']
        posts = Post.objects.all()
        posts = posts.filter(tags__content=tag_content)
        try:
            self.check_object_permissions(self.request, posts)
        except:
            raise PermissionDenied("You don't have permission of this method.")

        return posts
