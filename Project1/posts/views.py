from django.shortcuts import render

from rest_framework import generics
from .permissions import IsCreatorOrReadOnly
from .models import Post
from .serializers import PostDetailSerializer, PostDetailSerializer

from posts.serializers import PostListSerializer
# Create your views here.
class PostListView(generics.ListAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    # Post의 description을 앞 300자만 보내야 함
    def get_exception_handler(self):

class PostCreateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def get_exception_handler(self):

    # Post의 detail을 가지고 올 때 comment의 리스트를 가지고 올 수 있도록 할 수 있나?