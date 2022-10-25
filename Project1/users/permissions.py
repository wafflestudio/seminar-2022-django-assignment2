from rest_framework import permissions

from .models import User

class IsSuperUser(permissions.BasePermission):
    message = "Only Superuser have access"

    def has_permission(self, request, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.is_superuser == True

class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.is_superuser == True or request.user == obj
