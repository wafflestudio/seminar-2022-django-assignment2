from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import BlogPost, BlogComment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class BlogPostListSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = BlogPost
        fields = ['created_by', 'title', 'description', 'created_at', 'updated_at']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = BlogPost
        fields = ['created_by', 'title', 'description', 'created_at', 'updated_at']


class BlogCommentListSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    #post_id = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogPost.objects.all())
    is_updated = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = BlogComment
        fields = ['created_by', 'content', 'created_at', 'updated_at', 'is_updated']