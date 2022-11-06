from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views

from blog import models as blog_models
from blog import paginations as blog_paginations
from blog import permissions as blog_permissions
from blog import serializers as blog_serializers


def _delete_remained_tag(tag: blog_models.Tag):
    num_posts = len(blog_models.TagToPost.objects.filter(tag=tag.name))
    num_comments = len(blog_models.TagToComment.objects.filter(tag=tag.name))

    if num_posts + num_comments <= 1:
        tag.delete()


class PostListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = blog_paginations.PostListPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [blog_permissions.IsPostCreator]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer

    lookup_field = "pid"

    def perform_destroy(self, post: blog_models.Post):
        tags_to_post = blog_models.TagToPost.objects.filter(post__pid=post.pid)
        for ttp in tags_to_post:
            tag = blog_models.Tag.objects.get(name=ttp.tag.name)
            _delete_remained_tag(tag)
        post.delete()


class CommentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = blog_paginations.CommentListPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = blog_models.Comment.objects.all()
    serializer_class = blog_serializers.CommentSerializer

    def post(self, request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return super().get(request, *args, **kwargs)


class CommentUpdateDestroyView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [blog_permissions.IsCommentCreator]
    queryset = blog_models.Comment.objects.all()
    serializer_class = blog_serializers.CommentSerializer

    lookup_field = "cid"

    def put(self, request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return self.partial_update(request, *args, **kwargs)

    def perform_destroy(self, comment: blog_models.Comment):
        tags_to_comment = blog_models.TagToComment.objects.filter(
            comment__pid=comment.cid
        )
        for ttc in tags_to_comment:
            tag = blog_models.Tag.objects.get(name=ttc.tag.name)
            _delete_remained_tag(tag)
        comment.delete()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TagToPostListView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = blog_paginations.PostListPagination
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        tag = request.data["tag"]
        tag_to_post_list = blog_models.TagToPost.objects.filter(tag=tag)

        posts = []
        for tag_to_post in tag_to_post_list:
            pid = tag_to_post.post.pid
            posts.append(blog_models.Post.objects.get(pid=pid))

        serializer = blog_serializers.PostSerializer(posts, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class TagToCommentListView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = blog_paginations.CommentListPagination
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        tag = request.data["tag"]
        tag_to_comment_list = blog_models.TagToComment.objects.filter(tag=tag)

        comments = []
        for tag_to_comment in tag_to_comment_list:
            cid = tag_to_comment.comment.cid
            comments.append(blog_models.Comment.objects.get(cid=cid))

        serializer = blog_serializers.CommentSerializer(comments, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)