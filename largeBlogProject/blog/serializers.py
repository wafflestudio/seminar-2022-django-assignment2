from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from blog.models import Post, Comment, Tag


def update_tag(instance, tag_str):
    instance.tags.clear()
    for t in tag_str.replace(',', ' ').split():
        if not t:
            continue
        tag_obj, _ = Tag.objects.get_or_create(content=t.strip())
        instance.tags.add(tag_obj)
    instance.save()


class TaggedSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(write_only=True, allow_blank=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['tag'] = ', '.join(instance.tags.values_list('content', flat=True))
        return ret

    def create(self, validated_data):
        tag_str = validated_data.pop('tag', '')
        instance = self.Meta.model.objects.create(**validated_data)
        update_tag(instance, tag_str)
        return instance

    def update(self, instance, validated_data):
        tag_str = validated_data.pop('tag', '')
        super().update(instance, validated_data)
        update_tag(instance, tag_str)
        return instance


class PostSerializer(TaggedSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(PostSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['description'] = instance.description[:300]
        return ret


class CommentSerializer(TaggedSerializer):
    def update(self, instance, validated_data):
        validated_data['is_updated'] = True
        return super().update(instance, validated_data)

    class Meta:
        model = Comment
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data['username'],
          email=validated_data['email'],
          first_name=validated_data['first_name'],
          last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')
        extra_kwargs = {
          'first_name': {'required': True},
          'last_name': {'required': True}
        }
