from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Post, Comment, Tag, BlogUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        # ordering = 생성 역순
        # 단, 이때 descriptino의 글자 제한해야함
        fields = (
            'created_by',
            'created_at',
            'title',
            'summary_for_list_api'
        )
        model = Post


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'created_by',
            'created_at',
            'title',
            'description',
            'tag')
        model = Post
        extra_kwargs = {'tag': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('post', 'created_by', 'created_at', 'content', 'tag')
        model = Comment


class TagPostSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(many=True, read_only=True)

    class Meta:
        fields = ('name', 'created_at', 'content')
        model = Tag


class TagCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = ('name', 'created_at', 'content', 'post')
        model = Tag
        extra_kwargs = {'post': {'required': False}}
