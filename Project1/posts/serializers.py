from rest_framework import serializers

from posts.models import Post
from users.serializers import UserSerializer

class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def to_representation(self, instance):
        if len(instance.description) >= 300:
            instance.description = instance.description[:300]
        return instance

    class Meta:
        Model = Post
        fields = ['id', 'created_by', 'title', 'description']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.StringRelatedField(many=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'comments']