from rest_framework import serializers

from MediumBlog.models import Post, User, PostTag, Comment, CommentTag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user.username}

    class Meta:
        model = Post
        fields = ['title', 'id', 'created_by', 'created_at', 'updated_at', 'content', 'tags']


class PostListSerializer(serializers.ModelSerializer):
    CONTENT_LENGTH_LIMIT = 300
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if len(representation['content'])>self.CONTENT_LENGTH_LIMIT:
            representation['content'] = representation['content'][0:self.CONTENT_LENGTH_LIMIT]
        return representation

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'content', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['title', 'id', 'created_by', 'created_at', 'updated_at', 'content', 'tags']


class PostTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTag
        fields = ['content']


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    CONTENT_LENGTH_LIMIT = 300

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if len(representation['content'])>self.CONTENT_LENGTH_LIMIT:
            representation['content'] = representation['content'][0:self.CONTENT_LENGTH_LIMIT]
        return representation

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'post']


class CommentDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'tags']


class CommentTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentTag
        fields = ['content']
