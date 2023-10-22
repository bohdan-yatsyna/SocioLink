from rest_framework import permissions


class IsPostAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors of a post to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "author"):
            return obj.author == request.user

        return False
