from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)

    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     return {**internal_value, 'tags': data['content']}
    class Meta:
        model = Tag
        fields = '__all__'
    def __str__(self):
        return self.content