from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import CursorPagination

from .serializers import PostSerializer, CommentSerializer
from .serializers import PostDetailSerializer, CommentDetailSerializer
from .serializers import PostListSerializer, CommentListSerializer

from .permissions import IsOwner, IsUser

from .models import Post, Comment, User, Tag, TagToPostComment

from rest_framework import generics


# return "Tag" objects.
def get_tag_object(request) -> list:
    if 'tag' in request.data and request.data['tag']:
        tag_data = request.data['tag']
    else:
        tag_data = "No Tag"

    tag = []
    tag_data = tag_data.replace(" ", "")
    tag_lst = tag_data.split("#")
    for tag_data in tag_lst:
        if tag_data.strip() == "":
            continue
        try:
            tag.append(Tag.objects.get(content=tag_data))
        except Tag.DoesNotExist:
            tag.append(Tag.objects.create(content=tag_data))
    return tag


def delete_tag(tag_id):
    tags_content = TagToPostComment.objects.filter(tag_id=tag_id)
    if len(tags_content) == 1:
        last_tag = Tag.objects.get(content=tag_id)
        last_tag.delete()

# pagination class for post
class PostPagination(CursorPagination):
    ordering = 'updated_at'
    page_size = 20


# pagination class for comment
class CommentPagination(CursorPagination):
    ordering = 'created_at'
    page_size = 10


# post view for post, get
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsUser & IsOwner | IsAdminUser]
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostDetailSerializer
        return PostListSerializer

    def create(self, request, *args, **kwargs):
        tag = get_tag_object(request)
        request.data['tag_obj'] = tag

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# post view for patch, put, delete.
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsUser, IsOwner | IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        tags = TagToPostComment.objects.filter(post_id=kwargs['pk'])
        for tag in tags:
            delete_tag(tag.tag_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# comment view for post, get
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsUser & IsOwner | IsAdminUser]
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = super(CommentListCreateView, self).get_queryset()
        post_id = self.kwargs['post_id']
        return queryset.filter(post_id=post_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentDetailSerializer
        return CommentListSerializer

    def create(self, request, *args, **kwargs):
        post_id = Post.objects.get(pk=kwargs['post_id'])
        request.data['post_id'] = post_id

        tag = get_tag_object(request)
        request.data['tag_obj'] = tag

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# comment view for put, patch, delete.
class CommentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUser & IsOwner | IsAdminUser]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super(CommentUpdateDestroyView, self).get_queryset()
        pk = self.kwargs['pk']
        post_id = self.kwargs['post_id']
        return queryset.filter(pk=pk, post_id=post_id)

    def update(self, request, *args, **kwargs):
        request.data['is_updated'] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        tags = TagToPostComment.objects.filter(comment_id=kwargs['pk'])
        for tag in tags:
            delete_tag(tag.tag_id)
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostByTagListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = super(PostByTagListView, self).get_queryset()
        tag = self.kwargs['tag']
        return queryset.filter(tags=tag)


class CommentByTagListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = super(CommentByTagListView, self).get_queryset()
        tag = self.kwargs['tag']
        return queryset.filter(tags=tag)
