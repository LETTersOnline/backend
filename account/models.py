from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.constants import UserType


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username,
                          email=self.normalize_email(email)
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.user_type = UserType.SUPER_ADMIN
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    支持邮箱或用户名或学号登陆
    支持多种用户类型
    用户可以修改自己以及用户类型低于自己的所有用户的信息
    AbstractBaseUser:
        is_active:
        last_login:
    """
    objects = CustomUserManager()

    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_active = models.DateTimeField(auto_now=True)

    user_type = models.PositiveSmallIntegerField(choices=UserType.model_choices(), default=UserType.REGULAR)
    is_active = models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return "{}-{}".format(self.username, self.profile.fullname)

    def has_perm(self, perm, obj=None):
        # 仅仅超级管理员才有权限进入django admin
        if not self.is_active:
            return False
        return self.user_type == UserType.SUPER_ADMIN

    def has_module_perms(self, app_label):
        # 仅仅超级管理员才有权限进入django admin
        if not self.is_active:
            return False
        return self.user_type == UserType.SUPER_ADMIN

    @property
    def is_staff(self):
        # 仅仅超级管理员才有权限进入django admin
        if not self.is_active:
            return False
        return self.user_type == UserType.SUPER_ADMIN

    class Meta:
        ordering = ['id']


class Profile(models.Model):
    """
    user profile
    基于平台的用户属性以及拓展属性
    可为空或者有默认值
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    uid = models.CharField(max_length=64, blank=True, null=True)  # 标识号，可以是学号,座位号等，预留
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    fullname = models.CharField(max_length=128, default='佚名')
    school = models.CharField(max_length=200, blank=True, null=True)
    major = models.CharField(max_length=200, blank=True, null=True)
    mood = models.TextField(blank=True, null=True)

    accepted_number = models.IntegerField(default=0)
    total_score = models.BigIntegerField(default=0)
    submission_number = models.IntegerField(default=0)

    def add_accepted_problem_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save()

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save()

    # 计算总分时， 应先减掉上次该题所得分数， 然后再加上本次所得分数
    def add_score(self, this_time_score, last_time_score=None):
        last_time_score = last_time_score or 0
        self.total_score = models.F("total_score") - last_time_score + this_time_score

    # 留待扩展字段
    # extends = {
    #     'field_name1': 'field_value1',
    #     'field_name2': 'field_value2',
    #     ...
    # }
    extends = JSONField(default={}, blank=True, null=True)

    class Meta:
        ordering = ['id']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
