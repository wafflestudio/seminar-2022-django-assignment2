from knox.models import AuthToken
from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from blog.models import Post, Comment, PostTag, CommentTag
from blog.permissions import IsCreatorOrReadOnly, IsAuthenticatedOrReadOnly
from blog.serializers import PostListSerializer, PostDetailSerializer, CommentListSerializer, LoginUserSerializer, \
    UserSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CursorPagination

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly | IsAdminUser]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CursorPagination

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pk'])

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


class CommentRetrieveUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin,  GenericAPIView):
    permission_classes = [IsCreatorOrReadOnly | IsAdminUser]
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()

    def get_object(self):
        obj = Comment.objects.get(pk=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaggedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        tag = PostTag.objects.get(pk=self.kwargs['pk'])
        return Post.objects.filter(tag=tag)


class TaggedCommentListView(generics.ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        tag = CommentTag.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(tag=tag)
