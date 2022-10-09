from rest_framework import serializers
from .models import Post, Comment, Tag


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        # 단, 이때 descriptino의 글자 제한해야함
        fields = ('created_by', 'created_at', 'title', 'description')
        model = Post


class PostDetailSerialzier(serializers.ModelSerializer):
    class Meta:
        fields = ('created_by', 'created_at', 'title', 'description', 'tag')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('post', 'created_by', 'created_at', 'content', 'tag')
        model = Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'created_at', 'content')
        model = Tag
