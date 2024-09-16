from rest_framework.permissions import BasePermission


class IsGuestUser(BasePermission):
    """
    Custom permission to allow access only to guest users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_guest


class IsHostUser(BasePermission):
    """
    Custom permission to allow access only to host users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_host


class IsAdminUser(BasePermission):
    """
    Custom permission to allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsSuperUser(BasePermission):
    """
    Custom permission to allow access only to superusers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
