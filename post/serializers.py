from .models import Post, Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Comment
        fields = '__all__'

class CommentChangeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    updated = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
    def get_updated(self, request):
        return True

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ["post_id", "title", "author", "author_mail", "created_at", "updated_at", "content", "comments"]


class PostSummarySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ["post_id", "title", "author", "author_mail", "created_at", "updated_at", "content"]

    content = serializers.SerializerMethodField("get_sum_content")

    def get_sum_content(self, obj):
        return obj.content[:300]

