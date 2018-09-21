from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.constants import RegisterMethod
from account.models import User

from dynamic_preferences.registries import global_preferences_registry
global_preferences = global_preferences_registry.manager()


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return naturaltime(value)


class UserForAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    date_joined = CustomDateTimeField(read_only=True, required=False)
    date_active = CustomDateTimeField(read_only=True, required=False)

    class Meta:
        model = User


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    # 支持注册码
    code = serializers.CharField(max_length=20, required=False, allow_blank=True)

    date_joined = CustomDateTimeField(read_only=True, required=False)
    date_active = CustomDateTimeField(read_only=True, required=False)

    def validate(self, data):
        """
        Ensure the passwords are the same
        """
        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise serializers.ValidationError("The passwords have to be the same")
        return data

    def create(self, validated_data):
        # 注册用户
        if global_preferences['register__method'] == RegisterMethod.BAN:
            raise serializers.ValidationError(
                "Registration Forbidden, contact {}".format(global_preferences['admin_info']))

        code = validated_data.pop('code', None)
        if global_preferences['register__method'] == RegisterMethod.CODE:
            if code != global_preferences['register__code']:
                raise serializers.ValidationError(
                    "Register Code Invalid, contact {}".format(global_preferences['admin_info']))

        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'code',
                  'date_joined', 'date_active', 'user_type', 'is_active')
        read_only_fields = ('id', 'date_joined', 'date_active', 'user_type', 'is_active')


