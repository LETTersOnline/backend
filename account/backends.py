import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

from account.models import User
from account.serializers import UserMinimalSerializer


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
        'user': UserMinimalSerializer(user, context={'request': request}).data
    }


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    """
    自定义token验证中间件
    如果认证成功，发送登录成功信号
    """

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)
        # user, jwt_value = super(CustomJSONWebTokenAuthentication, self).authenticate(request)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return user, jwt_value
