from rest_framework.permissions import BasePermission

from TrainingOnline.constants import UserType
from account.models import User


class UserAdminOrOwner(BasePermission):
    """
    list            -> has_permission
    create          -> has_permission
    retrieve        -> has_permission -> has_object_permission
    update          -> has_permission -> has_object_permission
    delete          -> has_permission -> has_object_permission
    partial_update  -> has_permission -> has_object_permission

    list:                         允许认证用户进行操作
    create:                       允许所有用户进行操作
    retrieve:                     允许认证用户进行操作
    update,delete,partial_update: 允许对象所属用户或者用户等级高于对象所对应等级的用户进行操作
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return view.action in ['create', 'list', 'retrieve']
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return False

        if not request.user.is_authenticated:
            return False
        if request.user.user_type == UserType.SUPER_ADMIN:
            return True
        if view.action == 'retrieve':
            return True
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.user_type > obj.user.user_type
        if isinstance(obj, User):
            return request.user == obj or request.user.user_type > obj.user_type
        return False


class AuthPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type >= UserType.ADMIN

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type >= UserType.ADMIN
