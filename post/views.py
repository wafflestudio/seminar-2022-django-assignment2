from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostSummarySerializer, CommentChangeSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .permissions import CustomPermissionClass, CommentPermissionClass
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .pagination import CustomCursorPagination

#포스팅 목록 조회(비회원도)
class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSummarySerializer(queryset)
    permission_classes = (CustomPermissionClass,)
    pagination_class = CustomCursorPagination

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSummarySerializer(queryset, many=True)
        return Response(serializer.data)

#새 포스팅 작성
class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (CustomPermissionClass,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
      
from django.shortcuts import get_object_or_404

# 포스팅 내용 detail 조회, 수정, 삭제
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (CustomPermissionClass,)
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        return get_object_or_404(Post.objects.filter(post_id = pk))
      
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
       
        return Response(serializer.data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = (CommentPermissionClass,)
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post=post_id)

    
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (CommentPermissionClass,)
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentChangeSerializer

    def put(self, request, *args, **kwargs):
        updated = True
        serializer = CommentChangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(updated=updated)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    