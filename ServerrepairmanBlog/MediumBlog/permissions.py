from rest_framework import permissions

from MediumBlog.models import Post


class IsSafeOrAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsCreator(IsSafeOrAdminUser):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) or obj.created_by == request.user

    def has_permission(self, request, view):
        return True


class IsSafeOrAuthorizedUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            return request.user.is_authorized

        except:
            return False

