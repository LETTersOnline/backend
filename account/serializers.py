from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.constants import RegisterMethod
from account.models import User, Profile

from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return naturaltime(value)


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(max_length=64)
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)
    # 支持注册码
    code = serializers.CharField(max_length=20, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'code')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email exists")
        return value

    def validated_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        # Ensure the passwords are the same
        if data['password'] != data.pop('confirm_password', None):
            raise serializers.ValidationError("The passwords have to be the same")

        #  check register method
        if global_preferences['register__method'] == RegisterMethod.BAN:
            raise serializers.ValidationError(
                "Registration Forbidden, contact {}".format(global_preferences['admin_info']))

        code = data.pop('code', None)
        if global_preferences['register__method'] == RegisterMethod.CODE:
            if code != global_preferences['register__code']:
                raise serializers.ValidationError(
                    "Register Code Invalid, contact {}".format(global_preferences['admin_info']))

        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    id = serializers.IntegerField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_id(self, value):
        if User.objects.filter(id=value).exists():
            return value
        raise serializers.ValidationError("no such user")

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('uid', 'avatar', 'nickname', 'fullname', 'school', 'major', 'mood',
                  'accepted_number', 'total_score', 'submission_number')
        read_only_fields = ('accepted_number', 'total_score', 'submission_number')


class UserSerializer(serializers.ModelSerializer):
    date_joined = CustomDateTimeField()
    date_active = CustomDateTimeField()
    profile = UserProfileSerializer()

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        for k, v in profile_data.items():
            setattr(profile, k, v)
        profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile',
                  'date_joined', 'date_active', 'user_type', 'is_active')
        read_only_fields = ('id', 'username', 'date_joined', 'date_active', 'user_type', 'is_active')
