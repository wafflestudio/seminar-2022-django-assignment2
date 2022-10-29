from django.contrib.auth.models import User
from rest_framework import serializers

from medium.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['title', 'id', 'created_by', 'created_at', 'updated_at', 'description', 'image']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True, required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['title', 'id', 'created_by', 'created_at', 'updated_at', 'description', 'image']