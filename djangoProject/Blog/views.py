from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .serializers import *
from .models import Post, Comment
from .permissions import *


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        token = serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = {
        'GET': [AllowAny],
        'PUT': [IsCreator | IsAdminUser],
        'PATCH': [IsCreator | IsAdminUser],
        'DELETE': [IsCreator | IsAdminUser],
    }

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny]
        return [IsCreator | IsAdminUser]


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = {
        'GET': [AllowAny],
        'POST': [IsAuthenticated]
    }

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny]
        return [IsAuthenticated]


class CommentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentRetrieveUpdateDeleteSerializer
    permission_classes = [IsCreator | IsAdminUser]

    def get_object(self):
        queryset = self.get_queryset()
        objects = get_object_or_404(queryset, post=self.kwargs['ppk'], pk=self.kwargs['cpk'])
        self.check_object_permissions(self.request, objects)
        return objects

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_updated = True
        instance.save()
        return super().update(request,)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_updated = True
        instance.save()
        return super().put(request,)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_updated = True
        instance.save()
        return super().patch(request,)