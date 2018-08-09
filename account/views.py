from TrainingOnline import utils
from rest_framework import viewsets, parsers, status, decorators, response

from account import permissions
from account.models import User
from account.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.UserAdminOrOwner, ]
    serializer_class = UserSerializer
    pagination_class = utils.XPage
    # parser_classes = [parsers.MultiPartParser, ]
    queryset = User.objects.all()
