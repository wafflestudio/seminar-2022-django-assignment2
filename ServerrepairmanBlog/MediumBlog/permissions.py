from rest_framework import permissions

from MediumBlog.models import Post


class IsSafeOrAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class IsCreator(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj: Post):

        if super().has_object_permission(request, view, obj):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

    def has_permission(self, request, view):
        return True


class IsSafeOrAuthorizedUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        try:
#            print(request.user.is_authorized)
            return request.user.is_authorized

        except:
            return False

