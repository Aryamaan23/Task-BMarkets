from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
class CustomerAccessPermission(permissions.BasePermission):
    message="Adding customers not allowed"

    def has_permission(self, request, view):
        return request.method=='POST' or (
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated


"""
class BankAccessPermission(permissions.BasePermission):
    message="Adding customers not allowed"

    def has_permission(self, request, view):
        return request.method=='POST' or (
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated

"""


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
