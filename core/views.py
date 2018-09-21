from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()


class GetDynamicPreferences(GenericAPIView):
    permission_classes = []

    def get(self, request):
        data = {
            'registerMethod': global_preferences['register__method'],
            'adminInfo': global_preferences['admin_info'],
        }
        return Response(data)