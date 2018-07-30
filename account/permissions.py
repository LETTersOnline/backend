from rest_framework.permissions import BasePermission

from account.apps import UserType
from account.models import User


class AdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.user_type >= UserType.COACH:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if isinstance(obj, User):
            return obj == request.user
        return False


class AdvancedPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.user_type > obj.user.user_type
        if isinstance(obj, User):
            return request.user == obj or request.user.user_type > obj.user_type
        return False


class AdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type >= UserType.ADMIN
