from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser


class OnwerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return (
            request.user.is_authenticated
            and request.user.id == obj.id
            or request.user.is_superuser
        )
