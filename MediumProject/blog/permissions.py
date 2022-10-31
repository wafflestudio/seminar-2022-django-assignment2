from rest_framework import permissions
from .models import Post, Comment
from typing import Union


class IsCreatorOrReadOnly(permissions.BasePermission):
    message = {'Error': 'You cannot change the content of the post/comment that is not yours.'}

    def has_object_permission(self, request, view, obj: Union[Post, Comment]):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.created_by == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    message = {'Error': 'You should login/sign in to create a post'}

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_authenticated)


