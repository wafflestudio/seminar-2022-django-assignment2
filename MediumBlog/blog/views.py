from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from blog.models import Post, Comment, Tag
from blog.serializers import PostCreateSerializer, PostListSerializer, PostDetailSerializer, \
    CommentCreateSerializer, CommentListSerializer, RegistrationSerializer, PostCommentListSerializer, \
    PostListbyTagSerializer, CommentListbyTagSerializer, PostUpdateSerializer, CommentUpdateSerializer

from .permissions import IsPostCreator, IsCommentCreator


# Create your views here.
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = {
        'POST': PostCreateSerializer,
        'GET': PostListSerializer
    }
    permission_class = {
        'POST': [IsAuthenticated],
        'GET': [AllowAny]
    }

    def get_serializer_class(self):
        if self.request.method in self.serializer_class:
            return self.serializer_class.get(self.request.method)
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method in self.permission_class:
            permission_classes = self.permission_class.get(self.request.method)
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_class = {
        'PATCH': [IsPostCreator | IsAdminUser],
        'PUT': [IsPostCreator | IsAdminUser],
        'DELETE': [IsPostCreator | IsAdminUser],
        'GET': [AllowAny]
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        else:
            return PostUpdateSerializer

    def get_permissions(self):
        if self.request.method in self.permission_class:
            permission_classes = self.permission_class.get(self.request.method)
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        for tag in Tag.objects.all():
            if tag.posts.count() + tag.comments.count() == 1:
                tag.delete()

        return super().destroy(request, *args, **kwargs)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = {
        'POST': CommentCreateSerializer,
        'GET': CommentListSerializer
    }
    permission_class = {
        'POST': [IsAuthenticated],
        'GET': [AllowAny]
    }

    def get_serializer_class(self):
        if self.request.method in self.serializer_class:
            return self.serializer_class.get(self.request.method)
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method in self.permission_class:
            permission_classes = self.permission_class.get(self.request.method)
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)


class CommentUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsCommentCreator | IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        else:
            return CommentUpdateSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_updated = True
        instance.save()
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_updated = True
        instance.save()
        return super().patch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        for tag in Tag.objects.all():
            print(tag.content)
            print(tag.posts.count())
            if tag.posts.count() + tag.comments.count() == 1:
                tag.delete()

        return super().destroy(request, *args, **kwargs)


class PostCommentRetrieveView(generics.ListAPIView):
    serializer_class = PostCommentListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.all().filter(post=self.kwargs['pk'])

class PostListbyTagView(generics.ListAPIView):
    serializer_class = PostListbyTagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.all().filter(tags=self.kwargs['content'])


class CommentListbyTagView(generics.ListAPIView):
    serializer_class = CommentListbyTagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.all().filter(tags=self.kwargs['content'])
