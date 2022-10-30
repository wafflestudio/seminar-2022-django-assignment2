from rest_framework import serializers

from .models import Post, Comment, Tag


class PostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(PostSerializer):
    def to_representation(self, data):
        representation_value = super().to_representation(data)
        return {**representation_value, 'description': data.description[:300]}

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags']
        # fields = '__all__'


class PostDetailSerializer(PostSerializer):
    tag = serializers.CharField(max_length=100, read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value,
                'created_by': self.context['request'].user,
                'tags': data['tag_obj']}

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'like', 'tag']


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = '__all__'


class CommentListSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'updated_at', 'like', 'is_updated', 'tags']


class CommentDetailSerializer(CommentSerializer):
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value,
                'created_by': self.context['request'].user,
                'post_id': data['post_id'],
                'tags': data['tag_obj']}

    class Meta:
        model = Comment
        fields = ['id', 'content', 'is_updated']
