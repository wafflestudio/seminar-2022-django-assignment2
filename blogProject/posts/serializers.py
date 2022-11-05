from rest_framework import serializers

from posts.models import Post, Comment


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


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    # post = serializers.ReadOnlyField(source='post.id')
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'created_at', 'updated_at', 'is_updated']
