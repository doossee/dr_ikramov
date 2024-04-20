from rest_framework import permissions

from src.management.models import Admin, Doctor, Patient


class IsAdmin(permissions.BasePermission):
    """ """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and isinstance(user, Admin)


class IsDoctor(permissions.BasePermission):
    """ """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and isinstance(user, Doctor)


class IsPatient(permissions.BasePermission):
    """ """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and isinstance(user, Patient)