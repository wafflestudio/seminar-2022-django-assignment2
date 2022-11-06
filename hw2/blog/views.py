from django.http import Http404
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response

from blog.models import Post, Comment
from blog.serializers import PostDetailSerializer, PostListSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from blog.permissions import IsWriterOrReadOnly
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class UserSignUpView(APIView):
    def post(self, request):
        user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({"Token": token.key})


class UserSignInView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})
        else:
            return Response(status=401)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsWriterOrReadOnly | IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsWriterOrReadOnly | IsAdminUser]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostCommentListView(APIView):

    def get(self, request, pk, format=None):
        comments = Comment.objects.filter(post=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

