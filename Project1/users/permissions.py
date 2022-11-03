from rest_framework import permissions

from .models import User

class IsNotLogin(permissions.BasePermission):
    message = "You are logged in. To create account, please logout."
    def has_object_permission(self, request, view, obj):
        return not bool(request.user.is_authenticated)
class IsSuperUser(permissions.BasePermission):
    message = "Only Superuser can access."
    def has_object_permission(self, request, view, obj:User):
        return request.user.is_superuser==True

class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj:User):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser==True
