from django.shortcuts import render

from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.response import Response

from .permissions import IsCreatorOrReadOnly
from .models import Post

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
    parser_classes = [MultiPartParser]
    serializer_class = PostCreateSerializer

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # model에서 참조하는 필드명인 듯?
    lookup_field = 'id'
    # url에서 갖고 오는 parameter명
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        try:
            post_id = self.kwargs['post_id']
            posts = Post.objects.all()
            post = posts.filter(id=post_id)
            if post is None:
                raise NotFound("There is no post like that.")
            self.check_object_permissions(self.request, post)
        except:
            raise PermissionDenied("You're not creator of this post.")

        return post

    # Post의 detail을 가지고 올 때 comment의 리스트를 가지고 올 수 있도록 할 수 있나?
