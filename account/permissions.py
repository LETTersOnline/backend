from rest_framework.permissions import BasePermission

from core.constants import UserType
from core.utils import deprecated
from account.models import User


@deprecated("split user admin or owner permission class")
class UserAdminOrOwner(BasePermission):
    """
    list            -> has_permission
    create          -> has_permission
    retrieve        -> has_permission -> has_object_permission
    update          -> has_permission -> has_object_permission
    delete          -> has_permission -> has_object_permission
    partial_update  -> has_permission -> has_object_permission

    list:                         允许所有用户进行操作
    create:                       允许所有用户进行操作
    retrieve:                     允许所有用户进行操作
    update,delete,partial_update: 允许对象所属用户或者用户等级高于对象所对应等级的用户进行操作
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return view.action in ['create', 'list', 'retrieve']
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        if not request.user.is_authenticated:
            return False

        # 超级管理员拥有所有权限
        if request.user.user_type == UserType.SUPER_ADMIN:
            return True

        # 只有超级管理员能删除
        if view.action == 'delete':
            return False

        # 如果用户等级高于修改用户，或者为自身，可以更新
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.user_type > obj.user.user_type
        if isinstance(obj, User):
            return request.user == obj or request.user.user_type > obj.user_type

        return False


class NoAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return view.action in ['create', 'list', 'retrieve']
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True


class AuthPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == UserType.SUPER_ADMIN

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type == UserType.SUPER_ADMIN


class OwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # # 不允许非管理员删除
        # if view.action == 'delete':
        #     return False

        # 如果用户等级高于修改用户，或者为自身，可以更新
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.user_type > obj.user.user_type
        if isinstance(obj, User):
            return request.user == obj or request.user.user_type > obj.user_type
        return False


class GetPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if not request.user.is_authenticated:
            return False
        # 如果用户等级高于修改用户，或者为自身，可以更新
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.user_type > obj.user.user_type
        if isinstance(obj, User):
            return request.user == obj or request.user.user_type > obj.user_type
        return request.user.user_type == UserType.SUPER_ADMIN
