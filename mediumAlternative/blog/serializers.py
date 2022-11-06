from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from blog.models import Post
from blog.models import Comment


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {**representation, 'created_by': representation.get('created_by')['username']}

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_by']
        read_only_fields = ['id']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id']


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('post')
        representation.update({'created_by': representation.get('created_by')['username']})
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user, 'post_id': self.context['post_pk']}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_by', 'is_updated']
        read_only_fields = ['id', 'is_updated', 'post']


class CommentDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'is_updated': True}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_by', 'created_at', 'updated_at', 'is_updated']
        read_only_fields = ['id', 'post', 'is_updated']
