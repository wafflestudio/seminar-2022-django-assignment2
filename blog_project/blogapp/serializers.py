from rest_framework import serializers
from blogapp.models import User, Post, Comment
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'description', 'created_at', 'updated_at', 'is_updated']


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'description', 'created_at']


class PostUpdateSerializer(PostSerializer):
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value['is_updated'] = True
        return {**internal_value, 'created_by': self.context['request'].user, 'updated_at': timezone.now()}


class PostDetailSerializer(PostSerializer):
    created_by = UserSerializer(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'content', 'created_at', 'updated_at', 'is_updated']


class CommentUpdateSerializer(CommentSerializer):
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value['is_updated'] = True
        return {**internal_value, 'created_by': self.context['request'].user, 'updated_at': timezone.now()}


class CommentDetailSerializer(CommentSerializer):
    created_by = UserSerializer(read_only=True)
