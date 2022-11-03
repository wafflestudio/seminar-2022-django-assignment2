from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView

from .models import Post, Comment
from .pagination import CustomCursorPagination
from .permissions import IsCreatorOrReadOnly
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializer
    pagination_class = CustomCursorPagination


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsCreatorOrReadOnly|IsAdminUser]
    lookup_field = 'post_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        pid = self.kwargs['post_id']
        return Comment.objects.filter(post__post_id=pid)


class CommentUpdateDestroyView(APIView):
    permission_classes = [IsCreatorOrReadOnly|IsAdminUser]

    def get_object(self):
        cid = self.kwargs.get('comment_id')
        try:
            comment = Comment.objects.get(comment_id=cid)
            self.check_object_permissions(self.request, comment)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def put(self, request, post_id, comment_id):
        comment = self.get_object()
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.validated_data['is_updated'] = True
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
