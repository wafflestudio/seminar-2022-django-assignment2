from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, TagToPost, TagToComment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']
        extra_kwargs = {
            'content': {'validators': []},
        }


class PostListSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    tag = TagSerializer(many=True, required=False)

    def create(self, validated_data):
        tag_list = validated_data.pop('tag', [])
        post = Post.objects.create(**validated_data)
        for tag_content in tag_list:
            dic = dict(tag_content)
            content = dic.get("content")
            tag = Tag.objects.get_or_create(content=content)[0]
            TagToPost.objects.get_or_create(tag=tag, post=post)
        return post

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
        fields = ['title', 'post_id', 'created_by', 'created_at', 'updated_at', 'description', 'tag']


class PostDetailSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = [
            'title',
            'post_id',
            'created_by',
            'created_at',
            'updated_at',
            'description',
            'image',
            'tag']


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    tag = TagSerializer(many=True, required=False)

    def create(self, validated_data):
        tag_list = validated_data.pop('tag', [])
        comment = Comment.objects.create(**validated_data)
        for tag_content in tag_list:
            dic = dict(tag_content)
            content = dic.get("content")
            tag = Tag.objects.get_or_create(content=content)[0]
            TagToComment.objects.get_or_create(tag=tag, comment=comment)
        return comment

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = [
            'post',
            'comment_id',
            'created_by',
            'created_at',
            'updated_at',
            'content',
            'is_updated',
            'tag']

