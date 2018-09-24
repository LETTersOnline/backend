from django.contrib.auth.password_validation import password_changed
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken, JSONWebTokenAPIView

from account.models import User
from account.permissions import OwnerPermission
from account.serializers import UserRegisterSerializer, ChangePasswordSerializer, UserSerializer, JWTLoginSerializer
from core.constants import UserType


class UserRegisterView(CreateAPIView):
    """
    用户注册API
    仅支持POST方法注册，成功返回204状态和用户ID
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserLoginView(ObtainJSONWebToken):
    """
    用户登陆API
    获取JWT token，保存在客户端
    """
    serializer_class = JWTLoginSerializer


class UserVerifyTokenView(JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = VerifyJSONWebTokenSerializer


class UpdatePasswordView(GenericAPIView):
    """
    修改密码API
    自己或者拥有高于目标权限的用户可以调用
    """
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        aim_user = User.objects.get(id=serializer.data.get("id"))
        # check permission
        if user == aim_user or user.user_type > aim_user.user_type or user.user_type == UserType.SUPER_ADMIN:
            # Check old password if self
            if user == aim_user:
                old_password = serializer.data.get("old_password")
                if not user.check_password(old_password):
                    raise serializers.ValidationError(detail={'old_password': ['Wrong password.']})

            # set_password also hashes the password that the user will get
            aim_user.set_password(serializer.data.get("new_password"))
            aim_user.save()
            #     Inform all validators that have implemented a password_changed() method
            #     that the password has been changed.
            password_changed(serializer.data.get("new_password"))
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise serializer.PermissionDenied()


class UserRetrieveView(RetrieveAPIView):
    """
    查看用户信息API
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserUpdateView(RetrieveUpdateAPIView):
    """
    修改用户信息API
    """
    queryset = User.objects.all()
    permission_classes = [OwnerPermission]
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser]


class UserListView(ListAPIView):
    """
    列询用户信息API
    默认查询集为所有非管理员用户
    """
    queryset = User.objects.all().order_by('-profile__total_score')
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('username', 'profile__nickname', 'profile__fullname')
    search_fields = ('username', 'profile__nickname', 'profile__fullname')
