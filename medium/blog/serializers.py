from blog import models as blog_models
from rest_framework import serializers

POST_LIST_CONTENT_MAX_LENGTH = 300


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Post
        fields = "__all__"
        # lookup_field = "post_id"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    @classmethod
    def many_init(cls, *args, **kwargs):
        serializer = super().many_init(*args, **kwargs)
        for i, data in enumerate(serializer.data):
            serializer.data[i]["content"] = data["content"][
                :POST_LIST_CONTENT_MAX_LENGTH
            ]
        return serializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Comment
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }
