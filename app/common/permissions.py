from rest_framework import permissions


class IsWorker(permissions.BasePermission):
    """
    Checks if request user is worker(not hr or admin)
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return not request.user.is_manager


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
    Checks if request user is an admin
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin
