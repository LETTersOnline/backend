from TrainingOnline import utils
from rest_framework import viewsets, parsers, status, decorators, response, views

from account import permissions
from account.models import User
from account.serializers import UserForUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.UserAdminOrOwner, ]
    serializer_class = UserForUserSerializer
    pagination_class = utils.XPage
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, ]
    queryset = User.objects.all()


def UserManagerPermissionCheckView(request, format=None):
    pass