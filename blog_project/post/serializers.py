from rest_framework import serializers
from .models import Post, Comment, Tag


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'created_by',
            'created_at',
            'title',
            'summary_for_listing',
            'clapse_count',
            'comment_count'
        )
        model = Post


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'post',
            'created_by',
            'created_at',
            'content',
            'tags'
        )
        model = Comment


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'post',
            'created_by',
            'created_at',
            'updated_at',
            'is_updated',
            'create_tag',
            'content',
            'tags',
            'parent_comment'
        )
        model = Comment


class ClapseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'post',
            'created_by',
            'created_at'
        )


class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'created_at'
        )
        model = Tag


class TagCommentSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'name',
            'created_at',
            'content',
            'comment'
        )
        model = Tag
        extra_kwargs = {'comment': {'required': False}}


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagPostSerializer(
        many=True,
        required=False
    )

    class Meta:
        fields = (
            'created_by',
            'created_at',
            'updated_at',
            'title',
            'description',
            'n_min_read',
            'clapse_count',
            'comment_count',
            'create_tag',
            'tags',
            'summary_for_listing',
        )
        model = Post
