from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from blogapp.models import Post, Comment
from blogapp.permissions import IsCreatorOrReadOnly
from blogapp.serializers import PostSerializer, PostDetailSerializer, PostListSerializer,\
    CommentSerializer, CommentDetailSerializer, PostUpdateSerializer, CommentUpdateSerializer


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied
        return super().create(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all().order_by('-created_at')
        for query in queryset:
            query.description = query.description[0:300]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return PostUpdateSerializer
        return PostSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied
        return super().create(request, args, kwargs)

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Comment.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentDetailSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return CommentUpdateSerializer
        return CommentSerializer
