from rest_framework import permissions
from blog.models import Post, Comment
from typing import Union

class IsCreatorOrReadOnly(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj: Union[Post, Comment]):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.created_by == request.user