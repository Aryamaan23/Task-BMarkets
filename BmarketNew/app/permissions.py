from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
class CustomerAccessPermission(permissions.BasePermission):
    """
    Super users have all the permissions while the normal user have specific permissions
    """
    message="Adding customers not allowed"

    def has_permission(self, request, view):
        return request.method=='POST' or (
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated



class IsSuperUser(BasePermission):
    """
    Custom permission for the Bank, so that the superuser can only add the banks while the normal user can't
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
