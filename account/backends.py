from django.contrib.auth.backends import ModelBackend
from account.models import User


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
