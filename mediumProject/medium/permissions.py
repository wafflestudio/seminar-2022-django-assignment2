from rest_framework import permissions

from medium.models import Post


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
