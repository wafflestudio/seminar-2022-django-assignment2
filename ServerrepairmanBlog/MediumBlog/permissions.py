from rest_framework import permissions

from MediumBlog.models import Post


class IsSafeOrAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class IsPostCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return obj.created_by.is_authorized

        return obj.created_by == request.user

