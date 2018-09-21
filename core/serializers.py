# -*- coding: utf-8 -*-
# Created by crazyX on 2018/9/20
from django.contrib.auth import authenticate, user_logged_in, user_login_failed

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from account.models import User


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        print("fff", credentials)

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)
            print(user)
            if user:
                if not user.is_active:
                    # 发送登陆失败信号
                    user_login_failed.send(sender=user.__class__,
                                           credentials=credentials,
                                           request=self.context['request'])
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                # 发送登陆成功信号
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
                user = User.objects.get(id=user.id)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user,
                }
            else:
                # 发送登陆失败信号
                user_login_failed.send(sender=user.__class__,
                                       credentials=credentials,
                                       request=self.context['request'])
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
