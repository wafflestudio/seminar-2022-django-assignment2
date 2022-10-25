from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import User, UserFollowing



class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["id", "following_user_id", "created_at"]

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["id", "user_id", "created_at"]

class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    profile_photo = serializers.ImageField(required=False)
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-detail'
    )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        # 장고가 hashing 기능 제공
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
            # 비밀번호가 비었다는 에러를 raise해야 할듯


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'following', 'followers', 'profile_photo', 'posts']
        extra_kwargs = {"password": {"write_only": True}}

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_follower(self, obj):
        return FollowersSerializer(obj.following.all(), many=True).data