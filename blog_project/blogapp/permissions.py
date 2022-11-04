from rest_framework import permissions

from blogapp.models import Post


class IsCreatorOrReadOnly(permissions.BasePermission):
    message = 'You don\'t have permissions.'

    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user and (obj.created_by == request.user or request.user.is_staff)


class IsUser(permissions.BasePermission):
    message = 'You need to sign up first.'

    def has_object_permission(self, request, view, obj: Post):
        return False
