from django.contrib.auth.password_validation import validate_password
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse
from users.models import User, UserFollowing
from posts.models import Post

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, style={'input_type':'password', 'placeholder':'Password'},
                                     required=True, validators=[validate_password])
    password_verification = serializers.CharField(write_only=True, required=True,
                                                  style={'input_type':'password', 'placeholder':'Password_verification'})
    class Meta:
        model = User
        fields = ["id", "username", "password", "password_verification", "email"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_verification']:
            raise serializers.ValidationError({"password": "Password didn't match with password_verification."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class CreateDestroyFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["id", "user_id", "following_user_id", "created_at"]

     # 이미 팔로우 되어 있었다면 다시 팔로우 불가하도록
    # def validate(self, data):
    #     following_list = UserFollowing.objects.filter(user_id=self.context.get('request'))
    #     if self.context['request'].user == data['following_user']:
    #         raise serializers.ValidationError({'user_id': "You can't follow you."})
    #     elif self.context.get('request') in following_list:
    #         raise serializers.ValidationError({'following_user_id': "Already following."})
    #     return data

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'user': self.context['request'].user, 'following_user': data['following_user']}

class UserHyperlinkById(serializers.HyperlinkedRelatedField):
    view_name = 'user-detail'
    def to_representation(self, value):
        return 'username: %s - profile_link: %s' % (value.username, reverse('user-detail', args=[value.username], request=self.context['request']))

# class FollowingNumberSerializer(serializers.ModelSerializer):
#     the_number_of_following = serializers.IntegerField(read_only=True)
#
#     class Meta:
#
# class FollowersNumberSerializer(serializers.ModelSerializer):
#     the_number_of_followers = serializers.IntegerField(read_only=True)
#
#     class Meta:

# method 구분하여서 to_representation의 리턴값 다르게?
class FollowingSerializer(serializers.ModelSerializer):
    following_users = serializers.HyperlinkedRelatedField(read_only=True, lookup_field='username', view_name='user-detail')

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation['following_users'] = []

        if isinstance(instance, UserFollowing):
            representation['following_users'].append('username: %s - profile_link: %s' \
                                                     % (instance.following_user.username, reverse('user-detail', args=[instance.following_user.username],
                                                                                           request=self.context['request'])))
        elif isinstance(instance, QuerySet):
            for element in instance:
                representation['following_users'].append('username: %s - profile_link: %s' \
                                                        % (element.following_user.username, reverse('user-detail', args=[element.following_user.username],
                                                                                            request=self.context['request'])))
        else:
            raise serializers.ValidationError({"instance: instance is not proper type."})

        return representation

    class Meta:
        model = UserFollowing
        fields = ["id", "following_users", "created_at"]

class FollowersSerializer(serializers.ModelSerializer):
    followers = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model = UserFollowing
        fields = ["id", "followers", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation['followers'] = []
        if isinstance(instance, UserFollowing):
            representation['followers'].append('username: %s - profile_link: %s' \
                                                     % (instance.user.username,
                                                        reverse('user-detail', args=[instance.user.username],
                                                                request=self.context['request'])))
        elif isinstance(instance, QuerySet):
            for element in instance:
                representation['followers'].append('username: %s - profile_link: %s' \
                                                         % (element.user.username, reverse('user-detail',
                                                                                                     args=[
                                                                                                         element.user.username],
                                                                                                     request=
                                                                                                     self.context[
                                                                                                         'request'])))
        else:
            raise serializers.ValidationError({"instance: instance is not proper type."})
        return representation
class PostHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'post-detail'

    def to_representation(self, value):
        post_id = value.id
        return 'title: %s - url: %s' % (value.title, reverse('post-detail', args=[post_id], request=self.context['request']))

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type':'password', 'placeholder':'Password'}
    )
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    profile_photo = serializers.ImageField(required=False)
    is_superuser = serializers.BooleanField(read_only=True)
    posts = PostHyperlink(
        many=True,
        read_only=True,
        view_name='post-detail'
    )

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # User.objects.update()
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'following', 'followers', 'profile_photo', 'posts', 'is_superuser']
        extra_kwargs = {"password": {"write_only": True}}

    # obj에 profile view에서는 UserFollowing이 들어가고, following/follower view에서는 queryset이 들어옴
    def get_following(self, obj):
        return len(FollowingSerializer(obj.following.all(), context={'request':self.context['request']}, many=True).data)

    def get_followers(self, obj):
        return len(FollowersSerializer(obj.followers.all(), context={'request':self.context['request']}, many=True).data)