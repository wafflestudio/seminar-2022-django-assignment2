from rest_framework import serializers
from django.contrib.auth.models import User

from blog.models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        writer = serializers.ReadOnlyField(source='created_by.username')
        fields = '__all__'

    def to_representation(self, post):
        res = super().to_representation(post)
        res.update({'description': res['description'][:300]})
        return res


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        writer = serializers.ReadOnlyField(source='created_by.username')
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        writer = serializers.ReadOnlyField(source='created_by.username')
        fields = '__all__'



