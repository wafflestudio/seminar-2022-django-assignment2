from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from blog.models import Post, Comment, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    comfirm_password = serializers.CharField(
        write_only=True,
        required=True
    )
    def validate(self, data):
        if data['password'] != data['comfirm_password']:
            raise serializers.ValidationError(
                {'password' : "Password fields didn't match."}
            )
        return data

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'comfirm_password']

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']


class PostCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.CharField(allow_blank=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def create(self, validated_data):
        post = Post.objects.create(
            title=validated_data['title'],
            created_by=validated_data['created_by'],
            description=validated_data['description']
        )
        tag_list = validated_data.get('tags')
        for i in str(tag_list).split(sep=','):
            if i == '':
                continue
            tmp = i.strip()
            if Tag.objects.all().filter(content=tmp).count() == 0:
                tag = Tag.objects.create(content=tmp)
            else:
                tag = Tag.objects.get(content=tmp)
            post.tags.add(tag)
        return post

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'updated_at', 'description', 'tags']


class PostUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'updated_at', 'description']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def get_description(self, obj):
        return obj.description[:300]

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'created_at', 'updated_at', 'description', 'tags']


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'created_at', 'updated_at', 'description', 'comments', 'tags']


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    is_updated = serializers.BooleanField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated', 'tags']

class CommentUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    is_updated = serializers.BooleanField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']

class CommentCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.CharField(allow_blank=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def create(self, validated_data):
        comment = Comment.objects.create(
            post=validated_data['post'],
            created_by=validated_data['created_by'],
            content=validated_data['content']
        )
        tag_list = validated_data.get('tags')
        for i in str(tag_list).split(sep=','):
            if i == '':
                continue
            tmp = i.strip()
            if Tag.objects.all().filter(content=tmp).count() == 0:
                tag = Tag.objects.create(content=tmp)
            else:
                tag = Tag.objects.get(content=tmp)
            comment.tags.add(tag)
        return comment

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_at', 'updated_at', 'content', 'tags']


class PostCommentListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']

class PostListbyTagSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    def get_description(self, obj):
        return obj.description[:300]

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_by', 'created_at', 'updated_at', 'description', 'tags']

class CommentListbyTagSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    is_updated = serializers.BooleanField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'created_by': self.context['request'].user}

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated', 'tags']
