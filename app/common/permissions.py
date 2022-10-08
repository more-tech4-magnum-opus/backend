from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Checks if request user is an admin or hr
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_manager


class IsAdmin(permissions.BasePermission):
    """
    Checks if request user is an admin or hr
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin
