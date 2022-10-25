from rest_framework import serializers

from comments.models import Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    written_by = UserSerializer(read_only=True)

    def to_representation(self, instance):
        if len(instance.content) >= 300:
            instance.content = instance.cotent[:300]
        return instance

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'written_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'content', 'written_by', 'order', 'is_updated', 'post']