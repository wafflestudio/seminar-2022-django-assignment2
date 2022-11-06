from rest_framework import permissions
from .models import Post


class IsAdminOrCreatorOrReadOnly(permissions.BasePermission):
    message = 'It is allowed only Admin or Creator.'

    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser or obj.created_by == request.user
