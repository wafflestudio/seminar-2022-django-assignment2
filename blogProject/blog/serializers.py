from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    # user_info = UserSerializer(source='created_by', read_only=True)
    tags = TagSerializer(many=True, required=False)

    # POST 내용은 List 요청 시 최대 앞 300자만 보낸다
    # to_representation 메서드에서 description 을 300자로 자르는 것이 좋은가
    # 혹은 views.py 에서 get 함수 자체에서 description 을 300자로 잘라 보내는 것이 좋은가
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = instance.description[:300]
        representation['created_by'] = instance.created_by.username
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def create(self, validated_data):
        try:
            tags_data = validated_data.pop('tags')
        except KeyError:
            return super().create(validated_data)

        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            try:
                tag = Tag.objects.get(content=tag_data['content'])
            except Tag.DoesNotExist:
                tag = Tag.objects.create(**tag_data)
            finally:
                TagToPostOrComment.objects.create(post_id=post.id, tag_id=tag.id)
        return post

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'tags']


class PostDetailSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='created_by', read_only=True)
    tags = TagSerializer(many=True, required=False)

    # Comment.objects.filter().count() 를 통해 Comment 개수를 세어 'number_of_comments' 값으로 출력
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['number_of_comments'] = Comment.objects.filter(post_id=instance.pk).count()
        return representation

    def update(self, instance, validated_data):
        try:
            tags_data = validated_data.pop('tags')
        except KeyError:
            return super().update(validated_data)

        post = Post.objects.get(id=instance.id)
        TagToPostOrComment.objects.filter(post_id=post.id).delete()
        for tag_data in tags_data:
            try:
                tag = Tag.objects.get(content=tag_data['content'])
            except Tag.DoesNotExist:
                tag = Tag.objects.create(**tag_data)
            finally:
                TagToPostOrComment.objects.create(post_id=post.id, tag_id=tag.id)
        return post

    class Meta:
        model = Post
        fields = ['user_info', 'title', 'description', 'created_at', 'updated_at', 'tags']


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.IntegerField(source='post.id', read_only=True)
    tags = TagSerializer(many=True, required=False)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = instance.created_by.username

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'post': Post.objects.get(id=self.context['post']), 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'tags']


class CommentDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user_info = UserSerializer(source='created_by', read_only=True)
    post = serializers.IntegerField(source="post.id", read_only=True)
    is_updated = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True, required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if self.context['request'] == 'POST':
            internal_value = {**internal_value, 'is_updated': True}
        return {**internal_value, 'is_updated': True}

    class Meta:
        model = Comment
        fields = ['id', 'user_info', 'post', 'content', 'created_at', 'updated_at', 'is_updated', 'tags']
