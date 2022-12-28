from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import Post, Comment, MyUser, PostTag, CommentTag
from MediumProject import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], validated_data['password'],
                                          validated_data['first_name'], validated_data['last_name'])
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Log Info.")

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['email', 'password']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    tag = serializers.CharField(max_length=10, allow_blank=True, write_only=True)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res.update({'content': instance.content[:300]})
        return res

    def update(self, instance, validated_data):
        validated_data['tag'] = instance.tag
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    def create(self, validated_data):
        if validated_data['tag'] == '':
            validated_data['tag'] = PostTag.objects.get_or_create(content="none")[0]
        else:
            validated_data['tag'] = PostTag.objects.get_or_create(content=validated_data['tag'])[0]
        validated_data['created_by'] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'description', 'content', 'tag', 'created']
        read_only_fields = ['id', 'created_by']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tag = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'description', 'content', 'tag', 'comments', 'created', 'updated']


class CommentListSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length=10, allow_blank=True, write_only=True)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res.update({'content': instance.content[:100]})
        return res

    def update(self, instance, validated_data):
        validated_data['tag'] = instance.tag
        instance = super().update(instance, validated_data)
        instance.is_updated = True
        instance.save()
        return instance

    def create(self, validated_data):
        if validated_data['tag'] == '':
            validated_data['tag'] = CommentTag.objects.get_or_create(content="none")[0]
        else:
            validated_data['tag'] = CommentTag.objects.get_or_create(content=validated_data['tag'])[0]
        validated_data['post'] = Post.objects.get(id=self.context['view'].kwargs['pk'])
        validated_data['created_by'] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'tag', 'created', 'is_updated']
        read_only_fields = ['id', 'created_by', 'is_updated']
