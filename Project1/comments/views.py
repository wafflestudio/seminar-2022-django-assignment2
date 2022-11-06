from django.shortcuts import render

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import CursorPagination
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Comment
from .serializers import CommentListCreateSerializer, CommentUpdateDestroySerializer
from .permissions import IsWriter
# Create your views here.
class StandardCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = 'id'
    ordering = '-created_at'
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardCursorPagination

    def get_queryset(self):
        try:
            comment_list = Comment.objects.filter(post__id=self.kwargs['post_id'])
            self.check_object_permissions(self.request, comment_list)
        except:
            raise NotFound("There is no post.")
        return comment_list

class CommentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsWriter]
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateDestroySerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        comments = Comment.objects.all()
        comment = comments.filter(id=comment_id)
        if len(comment) == 0:
            raise NotFound("There is no comment like that.")
        try:
            self.check_object_permissions(self.request, comment[0])
        except:
            raise PermissionDenied("You're not writer of this comment.")

        return comment

class CommentListByTagView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListCreateSerializer
    lookup_field = 'content'
    lookup_url_kwarg = 'content'


    def get_queryset(self):
        tag_content = self.kwargs['content']
        comments = Comment.objects.all()
        comments = comments.filter(tags__content=tag_content)
        try:
            self.check_object_permissions(self.request, comments)
        except:
            raise PermissionDenied("You don't have permission of this method.")
        return comments

class CommentListByTagViewInCurrentPost(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListCreateSerializer
    lookup_field = 'content'
    lookup_url_kwarg = 'content'


    def get_queryset(self):
        tag_content = self.kwargs['content']
        comments = Comment.objects.all()
        comments = comments.filter(tags__content=tag_content)
        try:
            self.check_object_permissions(self.request, comments)
        except:
            raise PermissionDenied("You don't have permission of this method.")
        return comments


