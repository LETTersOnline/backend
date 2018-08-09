from django.contrib.auth.backends import ModelBackend
from account.models import User
from account.serializers import UserSerializer


class AuthBackend(ModelBackend):
    """
    自定义认证后端
    支持用户名/邮箱+密码认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        users = (User.objects.filter(username=username) |
                 User.objects.filter(email=username)
                 ).distinct()
        for user in users:
            if user.check_password(password):
                return user
        return None


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt后端序列化函数
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
