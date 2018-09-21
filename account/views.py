from dynamic_preferences.registries import global_preferences_registry
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import ObtainJSONWebToken
from django.contrib.auth.password_validation import password_changed
from account.models import User
from account.serializers import UserRegisterSerializer, ChangePasswordSerializer, UserSerializer
from core.constants import UserType
from core.generics import APIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from core.serializers import JWTSerializer

global_preferences = global_preferences_registry.manager()


class UserRegisterAPI(CreateAPIView):
    """
    用户注册API
    仅支持POST方法注册，成功返回204状态和用户ID
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class ObtainJWTView(ObtainJSONWebToken):
    """
    用户登陆API
    获取JWT token，保存在客户端
    """
    serializer_class = JWTSerializer


class UpdatePasswordAPI(APIView):
    """
    修改密码API
    自己或者拥有高于目标权限的用户可以调用
    """
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return self.invalid_serializer(serializer)
        else:
            aim_user = User.objects.get(id=serializer.data.get("id"))
            # check permission
            if user == aim_user or user.user_type > aim_user.user_type or user.user_type == UserType.SUPER_ADMIN:
                # Check old password if self
                if user == aim_user:
                    old_password = serializer.data.get("old_password")
                    if not user.check_password(old_password):
                        return self.error(err='invalid-old_password',
                                          msg='old_password: Wrong password.',
                                          status_code=status.HTTP_400_BAD_REQUEST)

                # set_password also hashes the password that the user will get
                aim_user.set_password(serializer.data.get("new_password"))
                aim_user.save()
                #     Inform all validators that have implemented a password_changed() method
                #     that the password has been changed.
                password_changed(serializer.data.get("new_password"))
                return self.success(status_code=status.HTTP_204_NO_CONTENT)
            else:
                return self.error(msg='no permission to access or modify resources.',
                                  status_code=status.HTTP_403_FORBIDDEN)


class ViewUpdateUserAPI(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().filter(is_active=True)


class GetDynamicPreferences(APIView):
    permission_classes = []

    def get(self, request):
        data = {
            'registerMethod': global_preferences['register__method'],
            'adminInfo': global_preferences['admin_info'],
        }
        return self.success(data)



