from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'created_at', 'updated_at']


class PostSummarySerializer(PostSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['content'] = representation['content'][:300]
        return representation
