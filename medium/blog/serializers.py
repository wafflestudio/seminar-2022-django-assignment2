from typing import Dict, List

from rest_framework import serializers

from blog import models as blog_models

_POST_LIST_CONTENT_MAX_LENGTH = 300


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(method_name="is_named_tags")
    tag_names = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=10),
        write_only=True,
        source="tags",
        required=False,
    )

    def is_named_tags(self, post: blog_models.Post) -> List[str]:
        tags_to_post = blog_models.TagToPost.objects.filter(post__pid=post.pid)
        return [ttp.tag.name for ttp in tags_to_post]

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

        for tag_name in tags_data:
            tag, _ = blog_models.Tag.objects.get_or_create(name=tag_name)
            blog_models.TagToPost.objects.get_or_create(tag=tag, post=post)
        return post


class CommentSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(
        method_name="is_named_tags", read_only=True
    )
    tag_names = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=10),
        write_only=True,
        source="tags",
        required=False,
    )

    def is_named_tags(self, comment: blog_models.Comment) -> List[str]:
        tags_to_comment = blog_models.TagToComment.objects.filter(
            comment__cid=comment.cid
        )
        return [ttc.tag.name for ttc in tags_to_comment]

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

        for tag_name in tags_data:
            tag, _ = blog_models.Tag.objects.get_or_create(name=tag_name)
            blog_models.TagToComment.objects.get_or_create(tag=tag, comment=comment)
        return comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog_models.Tag
        fields = "__all__"
