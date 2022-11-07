import json

from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from MediumBlog import models
from MediumBlog.models import Post, User, PostTag, Comment, CommentTag
from MediumBlog.permissions import IsCreator, IsSafeOrAuthorizedUser
from MediumBlog.serializers import *
from django.db.utils import IntegrityError
from rest_framework.generics import get_object_or_404


class PostTagListView(generics.ListAPIView):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer


class CommentTagListView(generics.ListAPIView):
    queryset = CommentTag.objects.all()
    serializer_class = CommentTagSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)


def update_manytomany(manytomanyList, manytomanyClass, obj, **kwargs):
    for tag in manytomanyList:
        now_tag, created = manytomanyClass.objects.get_or_create(**tag)
        if not created:
            now_tag.save()
            obj.tags.add(now_tag)

    obj.save()


def update_posttag(tags, post):
    update_manytomany([{'content': tag} for tag in tags], PostTag, post)


def update_commenttag(tags, comment):
    update_manytomany([{'content': tag} for tag in tags], CommentTag, comment)


def delete_not_used_many_to_many(my_m2m_class, obj_name):
    tags = my_m2m_class.objects.all().annotate(tag_count=Count(obj_name))
    for tag in tags:
        if tag.tag_count == 0:
            tag.delete()


class PostPermissionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSafeOrAuthorizedUser]
    serializer_class = PostListSerializer
    queryset = Post.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['created_by'] = request.user

        post = Post(created_by=request.data['created_by'], created_at=timezone.now(),
                    title=request.data['title'], content=request.data['content'])
        post.save()

        update_posttag(request.data['tags'], post)

        serializer_post = PostListSerializer(post)
        response = Response(data=serializer_post.data)  # super().create(request, *args, **kwargs)
        return response


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreator]
    queryset = Post.objects.all().order_by('-created_at')

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        post = get_object_or_404(Post, id=kwargs['pk'])
        post.updated_at = timezone.now()
        post.is_updated = True
        if 'tags' in request.data:
            update_posttag(request.data['tags'], post)
            print(post)

        serializer_post = PostDetailSerializer(post)
        response = Response(data=serializer_post.data)
        # post = super().get_object()
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        delete_not_used_many_to_many(PostTag, 'post')
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostListSerializer


class PostPermissionListCreateViewByTag(PostPermissionListCreateView):
    http_method_names = ['get']

    def get_queryset(self):
        return Post.objects.filter(tags__content=self.kwargs['tag'])


class CommentPermissionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSafeOrAuthorizedUser]
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentListSerializer

    def post(self, request, *args, **kwargs):
        print(request)
        request.data['created_by'] = request.user
        post = Post.objects.get(id=request.data['post_id'])

        comment = Comment(post=post, created_by=request.data['created_by'],
                          created_at=timezone.now(), content=request.data['content'])
        comment.save()

        update_commenttag(request.data['tags'], comment)

        serializer_comment = CommentDetailSerializer(comment)
        response = Response(data=serializer_comment.data)  # super().create(request, *args, **kwargs)
        return response


class CommentPermissionListCreateViewByPost(CommentPermissionListCreateView):
    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])

    def post(self, request, *args, **kwags):
        request.data['post_id'] = self.kwargs['post_id']
        return super().post(request, *args, **kwags)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreator]
    queryset = Comment.objects.all()
    http_method_names = ['get', 'update', 'delete']

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        comment = get_object_or_404(Comment, id=kwargs['pk'])
        comment.updated_at = timezone.now()
        comment.is_updated = True
        if 'tags' in request.data:
            update_posttag(request.data['tags'], comment)
            print(comment)

        serializer_comment = CommentDetailSerializer(comment)
        response = Response(data=serializer_comment.data)
        # comment = super().get_object()
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        delete_not_used_many_to_many(CommentTag, 'comment')
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentDetailSerializer
        return CommentListSerializer


class SignupView(APIView):

    def post(self, request):
#        try:
            user = User.objects.create_user(username=request.data['id'], password=request.data['password'])
            user.save()

            token = Token.objects.create(user=user)
            return Response({"Token": token.key})

#        except IntegrityError:
#            raise Http404("Already Exist id")

#        except:
#            raise Http404("Register Failed")


class SigninView(APIView):

    def post(self, request):
        try:
            user = User.objects.get(username=request.data['id'])

            if user.check_password(request.data['password']):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"id": request.data['id'], "Token": token.key})
            else:
                raise Http404("password not found")

        except:
            raise Http404("Login Failed")
