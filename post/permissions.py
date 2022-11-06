from rest_framework import permissions

class CustomPermissionClass(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'PUT':
            return obj.author == request.user
        elif request.method == 'DELETE':
            return obj.author == request.user


class CommentPermissionClass(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'PUT':
            return obj.owner == request.user
        elif request.method == 'DELETE':
            return obj.owner == request.user
 