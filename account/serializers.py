from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers

from TrainingOnline.constants import RegisterMethod
from account.models import User


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return naturaltime(value)


class UserForAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    date_joined = CustomDateTimeField(read_only=True, required=False)
    date_active = CustomDateTimeField(read_only=True, required=False)

    class Meta:
        model = User


class UserForUserSerializer(serializers.ModelSerializer):
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
        if settings.REGISTER_METHOD == RegisterMethod.BAN:
            raise serializers.ValidationError("Registration Forbidden, {}".format(settings.SITE_CONTACT_STRING))
        code = validated_data.pop('code', None)
        if settings.REGISTER_METHOD == RegisterMethod.CODE:
            if code != settings.REGISTER_CODE:
                raise serializers.ValidationError("Register Code Invalid, {}".format(settings.SITE_CONTACT_STRING))
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'password', 'confirm_password', 'code',
                  'date_joined', 'date_active', 'user_type', 'is_active',
                  'uid', 'fullname', 'school', 'major', 'mood',
                  'accepted_number', 'total_score', 'submission_number')
        read_only_fields = ('id', 'date_joined', 'date_active', 'user_type', 'is_active',
                            'accepted_number', 'total_score', 'submission_number')


