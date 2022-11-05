import tags.models
from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError

from users.models import User
from posts.models import Post, TagToPost
from tags.models import Tag
from users.serializers import UserSerializer
from comments.serializers import CommentListCreateSerializer
from tags.serializers import TagSerializer

class UserHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'user-detail'
    def to_representation(self, value):
        user_id = value.pk
        username = User.objects.filter(id=user_id)[0].username
        return 'username: %s - profile_link: %s' % (username, reverse('user-detail', args=[username], request=self.context['request']))

class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True, min_length=50)
    created_by = UserHyperlink(read_only=True, lookup_field='username', view_name='user-detail')
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "description", "created_by", "tags"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['title'] == None:
            raise serializers.ValidationError({"title": "Title is required."})
        elif attrs['description'] == None:
            raise serializers.ValidationError({"description": "description is required."})
        return attrs

    def create(self, validated_data):
        post = Post.objects.create(title=validated_data['title'], description=validated_data['description'], created_by=self.context['request'].user)
        if 'tags' in validated_data:
            for tag in validated_data['tags']:
                if len(Tag.objects.filter(content=tag['content'])) == 0:
                    tag = Tag.objects.create(post=post, content=tag['content'])
                else:
                    tag = Tag.objects.filter(content=tag['content'])[0]
                if isinstance(tag, QuerySet):
                    post.tags.add(tag[0])
                else:
                    post.tags.add(tag)
        return post

class UserHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'user-detail'
    def to_representation(self, value):
        username = value.username
        return 'username: %s - profile_link: %s' % (value.username, reverse('user-detail', args=[username], request=self.context['request']))

class TagHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'post-by-tag'

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(self, data)
        return {**internal_value, 'tags': data['tags']}
    def to_representation(self, value):
        tag = value.content
        # 여러 태그 있으면 반복문 돌려야 하나?
        return 'tags: %s' % (tag)


class PostListSerializer(serializers.ModelSerializer):
    created_by = UserHyperlink(read_only=True, lookup_field='username', view_name='post-list')
    tags = TagSerializer(many=True)
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user, 'tags': data['tags']}

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        if len(instance.description) >= 300:
            representation['description'] = instance.description[:300]
        # representation['tags'] = TagSerializer(instance.tags).data
        return representation
    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'description', 'tags']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentListCreateSerializer(read_only=True, many=True)
    created_by = UserHyperlink(read_only=True, lookup_field="username", view_name='user-detail')
    tags = TagSerializer(many=True, required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user, 'tags': data['tags']}

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'description', 'comments', 'tags']

class TagToPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagToPost
        fields = "__all__"
    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     return {**internal_value, 'post_id':data.post.id, 'tag_id':data.tag.id}