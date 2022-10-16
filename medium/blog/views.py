from blog import models as blog_models
from blog import permissions as blog_permissions
from blog import serializers as blog_serializers
from rest_framework import generics, mixins, permissions


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [blog_permissions.IsPostCreator]
    queryset = blog_models.Post.objects.all()
    serializer_class = blog_serializers.PostSerializer
    lookup_field = "pid"


class CommentListCreateView(generics.ListCreateAPIView):
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
        return self.destroy(request, *args, **kwargs)
