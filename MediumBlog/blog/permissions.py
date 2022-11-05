from rest_framework import permissions

from blog.models import Post, Comment


class IsPostCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user

class IsCommentCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Comment):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user