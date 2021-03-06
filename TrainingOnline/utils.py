import logging
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView as View
from rest_framework.response import Response
from rest_framework.status import *

logger = logging.getLogger("")


class XPage(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def response(data, status_code):
    return Response(data, status=status_code)


class APIView(View):

    def success(self, data=None):
        return response({"error": None, "data": data}, HTTP_200_OK)

    def error(self, msg="error", err="error", status_code=HTTP_400_BAD_REQUEST):
        return response({"error": err, "data": msg}, status_code)

    def _serializer_error_to_str(self, errors):
        for k, v in errors.items():
            if isinstance(v, list):
                return k, v[0]
            elif isinstance(v, OrderedDict):
                for _k, _v in v.items():
                    return self._serializer_error_to_str({_k: _v})

    def invalid_serializer(self, serializer):
        k, v = self._serializer_error_to_str(serializer.errors)
        if k != "non_field_errors":
            return self.error(err="invalid-" + k, msg=k + ": " + v, status_code=HTTP_400_BAD_REQUEST)
        else:
            return self.error(err="invalid-field", msg=v, status_code=HTTP_400_BAD_REQUEST)

    def server_error(self):
        return self.error(err="server-error", msg="server error", status_code=HTTP_500_INTERNAL_SERVER_ERROR)
