from rest_framework import permissions
class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view)->bool:
        return request.method =='POST'or(
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj)->bool:
        return request.user and request.user.is_authenticated