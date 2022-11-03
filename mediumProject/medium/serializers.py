from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostListSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if len(ret['description']) >= 300:
            ret['description'] = ret['description'][:300]
        return ret

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['title', 'post_id', 'created_by', 'created_at', 'updated_at', 'description']


class PostDetailSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['title', 'post_id', 'created_by', 'created_at', 'updated_at', 'description', 'image']


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['post', 'comment_id', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']

