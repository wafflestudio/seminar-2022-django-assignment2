from rest_framework import serializers
from rest_framework.reverse import reverse

from posts.models import Post
from users.serializers import UserSerializer
from comments.serializers import CommentListCreateSerializer
from tags.serializer import TagSerializer

class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True, min_length=50)
    created_by = UserSerializer(read_only=True)
    tags = TagSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "description", "created_by", "tags"]

    def validate(self, attrs):
        if attrs['title'] == None:
            raise serializers.ValidationError({"title": "Title is required."})
        elif attrs['description'] == None:
            raise serializers.ValidationError({"description": "description is required."})

        return attrs

    def create(self, validated_data):
        post = Post.objects.create(title = validated_data['title'],
                                   description = validated_data['description'],
                                   created_by=self.context['request'].user,
                                   )

        post.save()

        return post

class UserHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'user-detail'
    def to_representation(self, value):
        username = value.username
        return 'username: %s - profile_link: %s' % (value.username, reverse('user-detail', args=[username], request=self.context['request']))


class PostListSerializer(serializers.ModelSerializer):
    created_by = UserHyperlink(read_only=True, lookup_field='username', view_name='post-list')
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        if len(instance.description) >= 300:
            representation['description'] = instance.description[:300]
        return representation
    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'description']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentListCreateSerializer(read_only=True, many=True)
    created_by = UserHyperlink(read_only=True, lookup_field="username", view_name='user-detail')

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'description', 'comments']
