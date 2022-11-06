from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from MediumBlog import models
from MediumBlog.models import Post, User
from MediumBlog.permissions import IsPostCreator, IsSafeOrAdminUser
from MediumBlog.serializers import PostSerializer, PostDetailSerializer, PostListSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)


class PostPermissionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSafeOrAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['created_by'] = request.user
        return super().get(request, *args, **kwargs)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPostCreator]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer


class SignupView(APIView):

    def post(self, request):
        user = User.objects.create_user(username=request.data['id'], password=request.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({"Token": token.key})


class SigninView(APIView):

    def post(self, request):

        try:
            print(request.user)
            user = User.objects.get(username=request.data['id'])

            if user.check_password(request.data['password']):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"id": request.data['id'], "Token": token.key})
            else:
                raise Http404("password not found")

        except:
            raise Http404("Login Failed")
