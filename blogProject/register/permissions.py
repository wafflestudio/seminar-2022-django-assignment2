from rest_framework import permissions


class IsAdminOrAnonymous(permissions.BasePermission):
    message = 'It is allowed only Anonymous.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_anonymous


class IsAdminOrUser(permissions.BasePermission):
    message = 'It is allowed only Admin or User.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user
