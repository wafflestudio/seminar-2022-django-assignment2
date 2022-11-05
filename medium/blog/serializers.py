from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        hashed_password = make_password(validated_data['password'])
        user = User.objects.create_user(author=validated_data['username'], email=validated_data['email'], password=hashed_password)
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['__all__']

    def create(self, validated_data):
        description = validated_data.pop('description')
        instance = super().create(validated_data)
        setattr(instance, 'description_preview', description[:300])
        return instance


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'created', 'title', 'description_preview']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

