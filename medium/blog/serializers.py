from .models import *
from rest_framework import serializers


class PostListSerializer(serializers.ModelSerializer):
    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     return {**internal_value, 'created_by': self.context['request'].user}
    #
    # def to_representation(self, instance):
    #     if len(instance.description) >= 300:
    #         instance.description = instance.description[:300]
    #     return instance
    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     return {**internal_value, 'tag': self.context['request'].tag}

    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     tag = []
    #     for _, tag_name in enumerate(self.context['request'].tags):
    #         tags = Tag.objects.get_or_create(tag_name=tag_name)
    #         tag.append(tags)
    #     return {**internal_value, 'tag': tag, 'created_by': self.context['request'].user}

    class Meta:
        fields = [
            'id',
            'title',
            'created_by',
            'created_at',
            'summary',
            'read_time',
        ]
        model = Post


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'id',
            'tag_name',
            'created_at',
        ]
        model = Tag


class CommentSerializer(serializers.ModelSerializer):

    # tag = TagSerializer(many=True, read_only=True)

    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     tag = []
    #     for _, tag_name in enumerate(self.context['request'].tags):
    #         tags = Tag.objects.get_or_create(tag_name=tag_name)
    #         tag.append(tags)
    #     return {**internal_value, 'tag': tag}

    class Meta:
        fields = [
            'id',
            'post',
            'created_by',
            'created_at',
            'updated_at',
            'content',
            'is_updated',
            'is_activated',
            'like_count',
            'parent',
            'tag',
        ]
        model = Comment


class TagPostSerializer(serializers.ModelSerializer):

    # tag_post = PostListSerializer(many=True, read_only=True)

    class Meta:
        fields = [
            'tag_name',
            'tag_post',
        ]
        model = Tag


class TagCommentSerializer(serializers.ModelSerializer):

    # tag_comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = [
            'tag_name',
            'tag_comment',
        ]
        model = Tag


class PostDetailSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    # tag = TagSerializer(many=True, read_only=True)

    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        fields = [
            'id',
            'title',
            'tag',
            'created_by',
            'created_at',
            'updated_at',
            'read_time',
            'description',
            'url',
            'like_count',
            'comments',
        ]
        model = Post
