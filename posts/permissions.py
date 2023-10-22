from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from posts.models import Post


class IsPostAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors of a post to edit or delete it.
    """

    def has_object_permission(self, request: Request, view: View, obj: Post) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "author"):
            return obj.author == request.user

        return False
