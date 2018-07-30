from django.apps import AppConfig
from TrainingOnline.constants import Choices


class AccountConfig(AppConfig):
    name = 'account'


class UserType(Choices):
    REGULAR = 1  # 普通用户
    LETTERS = 2  # LETTers队员
    COACH = 3  # 教练
    ADMIN = 4  # 管理员
    SUPER_ADMIN = 5  # 超级管理员
