from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from blog.models import BlogPost, BlogComment
from blog.permissions import IsCreatorOrReadOnly
from blog.serializers import UserSerializer, BlogPostListSerializer, BlogPostDetailSerializer, \
    BlogCommentListSerializer


# Create your views here.
class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostListSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# class PostCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = BlogPost.objects.all()
#     serializer_class = BlogPostListSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDetailSerializer
    lookup_field = "pid"

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     queryset = self.filter_queryset(queryset)
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         filter[field] = self.kwargs[field]
    #
    #     return get_object_or_404(queryset, **filter)

    # def get_queryset(self):
    #     try:
    #         return BlogPost.objects.filter(id=)

    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     return super().put(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return super().delete(request, *args, **kwargs)


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentListSerializer
    lookup_field = 'pid'

    def get_object(self):
        obj = BlogComment.objects.get(pk=self.kwargs['pid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        #request.data['post'] = kwargs.get('pid')
        return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     print(request.data)
    #     print(kwargs.get("pid"))
    #     data = request.data
    #     data['post'] = kwargs.get("pid")
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user, post_id=self.kwargs['pid'])

    # def post(self, request, *args, **kwargs):
    #     request.data['post'] = kwargs.get('pid')
    #     return super().post(request, *args, **kwargs)


class CommentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentListSerializer

    def put(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)


