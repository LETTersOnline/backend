from rest_framework_jwt.views import ObtainJSONWebToken

from core.serializers import JWTSerializer


class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer


obtain_jwt_token = ObtainJWTView.as_view()
