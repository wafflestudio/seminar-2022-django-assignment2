from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'author', 'description']

    def create(self, validated_data):
        description = validated_data.pop('description')
        instance = super().create(validated_data)
        setattr(instance, 'description_preview', description[:300])
        return instance


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'created', 'title', 'description_preview', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

