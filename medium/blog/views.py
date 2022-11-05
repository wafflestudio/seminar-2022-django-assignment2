from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from blog.models import Signup, Login, Post, Comment
from blog.permissions import IsCreatorOrReadOnly
from blog.serializers import SignupSerializer, LoginSerializer, PostListSerializer, CommentSerializer, PostDetailSerializer



# Create your views here.

class SignUpView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Signup.objects.all()
    serializer_class = SignupSerializer
    def create(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = User.objects.create_user(username = self.request.data['username'],
                                            email = self.request.data['email'],
                                            password = self.request.data['password'])
                user.save()
                serializer.save()
                token = Token.objects.create(user=user)
                return Response("successfully signed up", status = status.HTTP_201_CREATED)
            return Response("data is not valid", status= status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Login.objects.all()
    serializer_class = LoginSerializer
    def post(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})
        else:
            return Response("User does not exist", status=status.HTTP_401_UNAUTHORIZED)

class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permissions_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def update(self, request, *args, **kwargs):
        is_updated = True
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(is_updated=is_updated)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

