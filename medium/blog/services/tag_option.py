import enum
from typing import List, Optional, Tuple, Type, Union

from django.db import models
from rest_framework import exceptions

from blog import models as blog_models


class TagOptions(str, enum.Enum):
    AND = "AND"
    OR = "OR"

    @classmethod
    def validate_option(cls, option_raw: str) -> Tuple[bool, str]:
        for option in cls:
            if option_raw.upper() == option:
                return True, option
        return False, option_raw

    @classmethod
    def tag_filter(
        cls,
        target_model: Type[models.Model],
        tag_list: List,
        initial_option: str,
    ) -> models.QuerySet[
        Optional[Union[blog_models.Post, blog_models.Comment]]
    ]:
        (is_valid, option) = cls.validate_option(initial_option)

        if not is_valid:
            raise exceptions.ValidationError(
                f"Option '{option}' is invalid. Option must be either 'or' or 'and'"
            )

        tag_names = [tag["name"] for tag in tag_list]

        if option == cls.AND:
            objects = target_model.objects.all()
            for tag_name in tag_names:
                objects = objects.filter(tags__name=tag_name)
        elif option == cls.OR:
            objects = target_model.objects.filter(
                tags__name__in=tag_names
            ).distinct()

        return objects
