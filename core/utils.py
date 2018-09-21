import logging
import functools
import inspect
import warnings
from collections import OrderedDict

from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView as View
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import GenericViewSet

logger = logging.getLogger("")

string_types = (type(b''), type(u''))


def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    if isinstance(reason, string_types):

        # The @deprecated is used with a 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated("please, use another function")
        #    def old_function(x, y):
        #      pass

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Call to deprecated class {name} ({reason})."
            else:
                fmt1 = "Call to deprecated function {name} ({reason})."

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):

        # The @deprecated is used without any 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated
        #    def old_function(x, y):
        #      pass

        func2 = reason

        if inspect.isclass(func2):
            fmt2 = "Call to deprecated class {name}."
        else:
            fmt2 = "Call to deprecated function {name}."

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))


class XPage(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def response(data, status_code):
    return Response(data, status=status_code)


class APIView(View):
    # 对drf APIView的简单封装，方便使用

    def success(self, data=None, status_code=HTTP_200_OK):
        return response({"error": None, "data": data}, status_code)

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


class SimpleModelViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()` and `list()` actions.
    """
    pass


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
