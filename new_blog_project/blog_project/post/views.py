from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from user import models as user_models
from user import serializers as user_serializers
from notification import views as notification_views

# Create your views here.


class PostList(APIView):

    def get(self, request, format=None):
        pass

    def post():
        pass


class PostDetail(APIView):

    def get():
        pass

    def put():
        pass

    def destroy():
        pass


class CommentList(APIView):

    def get():
        pass

    def post():
        pass


class CommentDetail(APIView):

    def put():
        pass

    def delete():
        pass


class ClapseList(APIView):

    def get():
        pass

    def post():
        pass


class UnClapseList(APIView):

    def destroy():
        pass


class TagPostList(APIView):

    def get():
        pass


class TagCommentList(APIView):

    def get():
        pass
