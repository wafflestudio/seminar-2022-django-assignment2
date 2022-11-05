from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.reverse import reverse

from users.models import User

from posts.models import Post

from comments.models import Comment

from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class UserHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'user-detail'
    def to_representation(self, value):
        user_id = value.pk
        username = User.objects.filter(id=user_id)[0].username
        return 'username: %s - profile_link: %s' % (username, reverse('user-detail', args=[username], request=self.context['request']))

class PostHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'post-detail'

    def to_representation(self, value):
        post_id = value.id
        post_title = Post.objects.filter(id=post_id)[0].title
        return 'title: %s - profile_link: %s' % (post_title, reverse('post-detail', args=[post_id], request=self.context['request']))

class CommentListCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    written_by = UserHyperlink(read_only=True, lookup_field='username', view_name='user-detail')
    post = PostHyperlink(read_only=True, lookup_field='id', lookup_url_kwarg='post_id', view_name='post-detail')
    tags =TagSerializer(many=True, required=False)

    def validate(self, attrs):
        if attrs['content'] == None:
            raise serializers.ValidationError({"content": "content is required."})
        return attrs

    def create(self, validated_data):
        comment = Comment.objects.create(content=validated_data['content'], written_by=self.context['request'].user, post=Post.objects.filter(id=validated_data['post_id'])[0])
        if 'tags' in validated_data:
            for tag in validated_data['tags']:
                if len(Tag.objects.filter(content=tag['content'])) == 0:
                    tag = Tag.objects.create(comment=comment, content=tag['content'])
                else:
                    tag = Tag.objects.filter(content=tag['content'])[0]
                if isinstance(tag, QuerySet):
                    comment.tags.add(tag[0])
                else:
                    comment.tags.add(tag)
        return comment


    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        if len(instance.content) >= 300:
            representation['content'] = instance.content[:300]
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'written_by': self.context['request'].user, 'post_id': self.context['view'].kwargs['post_id']}

    class Meta:
        model = Comment
        fields = ['id', 'content', 'written_by', 'is_updated', 'post', 'tags']
        extra_kwargs = {"is_updated": {"read_only": True}}

class CommentUpdateDestroySerializer(serializers.ModelSerializer):
    written_by = UserHyperlink(read_only=True, view_name='user-detail')
    tags = TagSerializer(read_only=True, required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'written_by': self.context['request'].user}

    def update(self, instance, validated_data):
        comment = super().update(instance, validated_data)
        comment.is_updated = True
        comment.save()

        return comment

    class Meta:
        model = Comment
        fields = ['id', 'content', 'written_by', 'is_updated', 'post', 'tags']
        extra_kwargs = {"is_updated": {"read_only": True}, "post": {"read_only": True}}