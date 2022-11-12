from typing import Dict

from rest_framework import serializers

from blog import models as blog_models

_POST_LIST_CONTENT_MAX_LENGTH = 300


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = blog_models.Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = blog_models.Post
        fields = "__all__"
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
                :_POST_LIST_CONTENT_MAX_LENGTH
            ]
        return serializer

    def create(self, validated_data: Dict):
        tags_data = validated_data.pop("tags", [])
        post = super().create(validated_data)

        for tag_data in tags_data:
            tag, _ = blog_models.Tag.objects.get_or_create(**tag_data)
            blog_models.TagToPost.objects.get_or_create(post=post, tag=tag)
        return post


class CommentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = blog_models.Comment
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create(self, validated_data: Dict):
        tags_data = validated_data.pop("tags", [])
        comment = super().create(validated_data)

        for tag_data in tags_data:
            tag, _ = blog_models.Tag.objects.get_or_create(**tag_data)
            blog_models.TagToComment.objects.get_or_create(comment=comment, tag=tag)
        return comment
