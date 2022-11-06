from django.db.models import QuerySet
from rest_framework import generics
import rest_framework.permissions as permission_set

from .permissions import IsAdminOrCreatorOrReadOnly
from .serializers import *
from .pagenations import *


def delete_unused_tag(tag_manytomany_queryset):
    for tag_manytomany_element in tag_manytomany_queryset:
        count = TagToPostOrComment.objects.filter(tag_id=tag_manytomany_element.tag_id).count()
        if count != 0:
            continue
        tag = Tag.objects.get(id=tag_manytomany_element.tag_id)
        try:
            tag.delete()
        except Tag.DoesNotExist:
            pass


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

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pid'])
        tag_manytomany_queryset = TagToPostOrComment.objects.filter(post_id=post.id)
        response = super().delete(request)
        delete_unused_tag(tag_manytomany_queryset)
        return response


class CommentView(generics.ListCreateAPIView):
    permission_classes = [permission_set.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    lookup_field = 'pid'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs[self.lookup_field])

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

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['cid'])
        tag_manytomany_queryset = TagToPostOrComment.objects.filter(comment_id=comment.id)
        response = super().delete(request)
        delete_unused_tag(tag_manytomany_queryset)
        return response


class TagListView(generics.ListAPIView):
    permission_classes = [permission_set.AllowAny]
    pagination_class = TagPagination
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PostFilteredByTagListView(generics.ListAPIView):
    pagination_class = PostPagination
    permission_classes = [permission_set.AllowAny]
    serializer_class = PostListSerializer
    lookup_field = 'content'

    def get_queryset(self):
        tag_id = Tag.objects.get(content=self.kwargs[self.lookup_field]).id
        posts_id = TagToPostOrComment.objects.filter(tag_id=tag_id, post_id__isnull=False)
        queryset = Post.objects.filter(id=0)
        for p in posts_id:
            queryset |= Post.objects.filter(id=p.post_id)
        return queryset


class CommentFilteredByTagListView(generics.ListAPIView):
    pagination_class = CommentPagination
    permission_classes = [permission_set.AllowAny]
    serializer_class = CommentSerializer
    lookup_field = 'content'

    def get_queryset(self):
        tag_id = Tag.objects.get(content=self.kwargs[self.lookup_field]).id
        comments_id = TagToPostOrComment.objects.filter(tag_id=tag_id, comment_id__isnull=False)
        queryset = Comment.objects.filter(id=0)
        for c in comments_id:
            queryset |= Comment.objects.filter(id=c.comment_id)
        return queryset