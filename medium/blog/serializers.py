from typing import Dict, List

from rest_framework import serializers

from blog import models as blog_models

_POST_LIST_CONTENT_MAX_LENGTH = 300


class TagSerializerField(serializers.CharField):
    ''' SerializerField To get tags which is included in Post or Comment w/o using ManyToManyField.

    Necessity:
        - There is no way to cover read & write at once with using serializers which are provided in DRF,
          when we try to implement Tag w/o ManyToManyField.
        - Since We didn't use ManyToManyField, we have to make a detour to read & write Tags with using 
          only one SerializerField.
        - TagSerializerField is implemented to cover above problems.

    TagSerializerField basically inherits serializers.CharField,
    but it is quite similar with serializers.SerializerMethodField.
    
        i. It has own validation checker.
        ii. It uses parents method to represent value.
            a) since tags field is not contained in Post or Comment,
               get_attribute function passed instance without any processes.
        iii. Since it is allowed to create Post or Comment w/o tags, validation order is modified.

    When you use TagSerializerField,
        Must:
            - You must implement get_tags or customized method for representation.
        Pros:
            - You can simply implement Serializer w/o many to many field.
            - You can use many functions which is contained in serializers.CharField w/o further implementations.
        Cons:
            - Since it is specialized with specific structure, it may be hard to do massive revision.
    '''

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        if self.method_name is None:
            self.method_name = "get_{field_name}".format(field_name=field_name)
        super().bind(field_name, parent)

    def run_validation(self, data):
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data
        for tag in data:
            if tag == "" or (self.trim_whitespace and str(tag).strip() == ""):
                if not self.allow_blank:
                    self.fail("blank")
                return ""
        value = self.to_internal_value(data)
        self.run_validators(value)
        return value

    def to_internal_value(self, data):
        if not (isinstance(data, list) and all(isinstance(tag, str) for tag in data)):
            self.fail("invalid")
        return data

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)
    
    def get_attribute(self, instance):
        return instance


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializerField(method_name="is_named_tags", required=False, max_length=10)

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
    tags = TagSerializerField(method_name="is_named_tags", required=False, max_length=10)

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
