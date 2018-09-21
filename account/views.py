
from rest_framework import viewsets, parsers, status
from rest_condition import Or

from core import utils
from account import permissions
from account.models import User
from account.serializers import UserSerializer, ChangePasswordSerializer

from dynamic_preferences.registries import global_preferences_registry
global_preferences = global_preferences_registry.manager()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [Or(permissions.NoAuthenticatedPermission,
                             permissions.AdminPermission,
                             permissions.OwnerPermission, ),
                          ]
    serializer_class = UserSerializer
    pagination_class = utils.XPage
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, ]
    queryset = User.objects.all()


class UpdatePassword(utils.APIView):
    """
    修改密码API
    默认permission_classes = ['rest_framework.permissions.IsAuthenticated']
    """
    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not user.check_password(old_password):
                return self.error(err='invalid-old_password',
                                  msg='old_password: Wrong password.',
                                  status_code=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return self.success(status_code=status.HTTP_204_NO_CONTENT)

        return self.invalid_serializer(serializer)


class GetDynamicPreferences(utils.APIView):
    permission_classes = []

    def get(self, request):
        data = {
            'registerMethod': global_preferences['register__method'],
            'adminInfo': global_preferences['admin_info'],
        }
        return self.success(data)


def UserManagerPermissionCheckView(request, format=None):
    pass
