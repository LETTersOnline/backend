from rest_framework import serializers
from django.conf import settings
from account.models import User
from TrainingOnline.constants import RegisterMethod


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    # 考虑支持注册码
    code = serializers.CharField(max_length=20, required=False)

    def validate(self, data):
        """
        Ensure the passwords are the same
        """
        if data['password']:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("The passwords have to be the same")
        return data

    def create(self, validated_data):
        # 注册用户
        if settings.REGISTER_METHOD == RegisterMethod.BAN:
            raise serializers.ValidationError("Registration Forbidden, {}".format(settings.SITE_CONTACT_STRING))
        code = validated_data.pop('code', None)
        if settings.REGISTER_METHOD == RegisterMethod.CODE:
            if code != settings.REGISTER_CODE:
                raise serializers.ValidationError("Register Code Invalid, {}".format(settings.SITE_CONTACT_STRING))
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'code',
                  'date_joined', 'date_active', 'user_type', 'is_active',
                  'uid', 'fullname', 'school', 'major', 'mood')
        read_only_fields = ('id', 'date_joined', 'date_active', 'user_type', 'is_active')


