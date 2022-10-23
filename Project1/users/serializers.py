from rest_framework import serializers
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

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'following', 'followers', 'profile_photo']
        extra_kwargs = {"password": {"write_only": True}}

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_follower(self, obj):
        return FollowersSerializer(obj.following.all(), many=True).data