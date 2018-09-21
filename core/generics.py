# -*- coding: utf-8 -*-
# Created by crazyX on 2018/9/21
from rest_framework.generics import GenericAPIView

from core.mixins import BaseHandleMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin


class APIView(GenericAPIView, BaseHandleMixin):
    # 对drf APIView的简单封装，方便使用
    pass


class CreateAPIView(CreateModelMixin,
                    GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveAPIView(RetrieveModelMixin,
                      GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RetrieveUpdateAPIView(RetrieveModelMixin,
                            UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
