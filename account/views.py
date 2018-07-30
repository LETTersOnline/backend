from rest_framework.permissions import AllowAny

from TrainingOnline import utils
from rest_framework import viewsets

from account import permissions
from account.models import User
from account.serializers import UserSerializer


class UserRegisterAPI(utils.APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        """
        User register api
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success("Succeeded")
        else:
            return self.invalid_serializer(serializer)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AdminOrOwner,)
    serializer_class = UserSerializer
    pagination_class = utils.XPage
    queryset = User.objects.all()
