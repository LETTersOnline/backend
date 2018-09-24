from django.contrib.auth import authenticate, user_login_failed, user_logged_in
from django.contrib.auth.password_validation import validate_password
from django.contrib.humanize.templatetags.humanize import naturaltime
from dynamic_preferences.registries import global_preferences_registry
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from account.models import User, Profile
from core.constants import RegisterMethod

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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class JWTLoginSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

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
    last_login = CustomDateTimeField()
    profile = UserProfileSerializer()

    def validate(self, attrs):
        print('attrs: ', attrs)
        print(attrs)
        for k in attrs:
            print(k, ': ', attrs[k])
        return attrs

    def update(self, instance, validated_data):
        print("validated data: ", validated_data)
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile
        print('profile: ', profile_data)
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
                  'date_joined', 'date_active', 'user_type', 'is_active', 'last_login')
        read_only_fields = ('id', 'username', 'date_joined', 'date_active', 'user_type', 'is_active', 'last_login')


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    exclude user profile
    only allow email writeable
    """
    date_joined = CustomDateTimeField()
    date_active = CustomDateTimeField()

    def update(self, instance, validated_data):
        if User.objects.filter(email=validated_data.get('email', None)).exclude(id=instance.id).exists():
            raise ValueError('email exist')
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'date_joined', 'date_active', 'user_type', 'is_active')
        read_only_fields = ('id', 'username', 'date_joined', 'date_active', 'user_type', 'is_active')


class UserRankSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    accepted_number = serializers.SerializerMethodField()
    submission_number = serializers.SerializerMethodField()

    def get_total_score(self, obj):
        return obj.profile.total_score

    def get_accepted_number(self, obj):
        return obj.profile.accepted_number

    def get_submission_number(self, obj):
        return obj.profile.submission_number

    def get_nickname(self, obj):
        return obj.profile.nickname

    def get_fullname(self, obj):
        return obj.profile.fullname

    def get_avatar(self, obj):
        return obj.profile.avatar

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'fullname', 'avatar',
                  'total_score', 'accepted_number', 'submission_number')
        read_only_fields = ('id', 'username', 'nickname', 'fullname', 'avatar',
                            'total_score', 'accepted_number', 'submission_number')
