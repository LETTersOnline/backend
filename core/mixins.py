# -*- coding: utf-8 -*-
# Created by crazyX on 2018/9/21
from collections.__init__ import OrderedDict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


class BaseHandleMixin(object):
    def success(self, data=None, status_code=HTTP_200_OK):
        return Response({"error": None, "data": data}, status_code)

    def error(self, msg="error", err="error", status_code=HTTP_400_BAD_REQUEST):
        return Response({"error": err, "data": msg}, status_code)

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


class CreateModelMixin(BaseHandleMixin):
    """
    Create a model instance.
    use serializer save method to create model
    return created model's id
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            created_model = serializer.save()
            return self.success(data={'id': created_model.id}, status_code=status.HTTP_201_CREATED)
        else:
            return self.invalid_serializer(serializer)


class RetrieveModelMixin(BaseHandleMixin):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success(serializer.data)


class UpdateModelMixin(BaseHandleMixin):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return self.success(data={'id': instance.id}, status_code=status.HTTP_201_CREATED)
        else:
            return self.invalid_serializer(serializer)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
