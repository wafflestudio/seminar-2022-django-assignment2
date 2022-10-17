from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostListSerializer, PostDetailSerializer, ClapseSerializer, TagCommentSerializer, TagPostSerializer, CommentDetailSerializer, CommentListSerializer
from .models import Post, Clapse, Comment, Tag
from user import models as user_models
from user import serializers as user_serializers
from user.permissions import IsAuthorOrReadOnly
from notification import views as notification_views

# Create your views here.


class PostList(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostListSerializer(
            post, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        created_by = request.user
        summary_for_listing = request.data["description"][:300]
        n_min_read = len(request.data["description"]) / 200
        serializer = PostDetailSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save(
                created_by=created_by,
                summary_for_listing=summary_for_listing,
                n_min_read=n_min_read
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class PostDetail(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        serializer = PostDetailSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):

        created_by = request.user
        post = Post.objects.get(pk=pk)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = PostDetailSerializer(
            post, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(created_by=created_by)
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        created_by = request.user
        post = Post.objects.get(pk=pk)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def post(self, request, pk, format=None):
        created_by = request.user
        post = Post.objects.get(pk=pk)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=created_by, post=post)
            notification_views.create_notification(
                created_by, post.created_by, 'comment', post, serializer.data['message']
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass


class ClapseList(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def get():
        pass

    def post():
        pass


class UnClapseList(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def destroy():
        pass


class TagPostList(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def get():
        pass


class TagCommentList(APIView):

    permission_class = (IsAuthorOrReadOnly, )

    def get():
        pass
