from rest_framework import permissions

from reviews.models import User as YamdbUser


class IsAdminAsDefinedByUserModel(permissions.BasePermission):
    """Allows access to users with admin rights"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Allows access only to administrators or read only."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Object level permission that allows access for writing to
    staff, moderators or object author
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.role == YamdbUser.MODERATOR
                or request.user == obj.author
            )
        ) or request.method in permissions.SAFE_METHODS
