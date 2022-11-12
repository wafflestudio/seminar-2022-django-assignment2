from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views

from blog import models as blog_models
from blog import paginations as blog_paginations
from blog import permissions as blog_permissions
from blog import serializers as blog_serializers
from blog.services import tag_option


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

    def delete(self, request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return self.destroy(request, *args, **kwargs)


class TagToPostListView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = blog_paginations.PostListPagination
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        tag_list = request.data["tags"]
        option = request.data.get("option", "and")

        posts = tag_option.TagOptions.tag_filter(
            blog_models.Post, tag_list, option
        )
        serializer = blog_serializers.PostSerializer(posts, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class TagToCommentListView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = blog_paginations.CommentListPagination
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        tag_list = request.data["tags"]
        option = request.data.get("option", "and")
        comments = tag_option.TagOptions.tag_filter(
            blog_models.Comment, tag_list, option
        )
        serializer = blog_serializers.CommentSerializer(comments, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
