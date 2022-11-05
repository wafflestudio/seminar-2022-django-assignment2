from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from .models import Post, Comment, Tag, TagToPost, TagToComment
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
    permission_classes = [IsCreatorOrReadOnly | IsAdminUser]
    lookup_field = 'post_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        comments = Comment.objects.filter(post=instance.post_id)
        tags = Tag.objects.filter(post=instance.post_id) | Tag.objects.filter(comment__in=comments.all())
        for tag in tags:
            num_post_with_this_tag_but_not_in_this_post = \
                TagToPost.objects.filter(tag=tag).exclude(post=instance.post_id).count()
            num_comment_with_this_tag_but_not_in_related_comments = \
                TagToComment.objects.filter(tag=tag).exclude(comment__in=comments.all()).count()
            if num_post_with_this_tag_but_not_in_this_post == 0 \
                    and num_comment_with_this_tag_but_not_in_related_comments == 0:
                tag_in_tag = Tag.objects.get(content=tag.content)
                tag_in_tag.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        pid = self.kwargs['post_id']
        return Comment.objects.filter(post__post_id=pid)


class CommentUpdateDestroyView(APIView):
    permission_classes = [IsCreatorOrReadOnly | IsAdminUser]

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
        tags = Tag.objects.filter(comment=comment)
        for tag in tags:
            tag_in_post = TagToPost.objects.filter(tag=tag)
            tag_in_comment = TagToComment.objects.filter(tag=tag)
            if len(tag_in_post)+len(tag_in_comment) == 1:
                tag_in_tag = Tag.objects.get(content=tag.content)
                tag_in_tag.delete()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagToPostView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        tag = self.kwargs['tag_content']
        return Post.objects.filter(tag=tag)


class TagToCommentView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        tag = self.kwargs['tag_content']
        return Comment.objects.filter(tag=tag)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return Response(status=status.HTTP_200_OK)
