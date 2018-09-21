# -*- coding: utf-8 -*-
# Created by crazyX on 2018/9/18
from django.forms import ValidationError

from dynamic_preferences.types import StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

from core.constants import RegisterMethod

register = Section('register')


@global_preferences_registry.register
class RegisterControl(StringPreference):
    section = register
    name = 'method'
    default = RegisterMethod.ANY

    def validate(self, value):
        if value not in RegisterMethod.choices():
            raise ValidationError('{} only'.format(RegisterMethod.choices()))


@global_preferences_registry.register
class RegisterCode(StringPreference):
    section = register
    name = 'code'
    default = ''


@global_preferences_registry.register
class SiteAdminInfo(StringPreference):
    name = 'admin_info'
    default = 'crazyX(xu_jingwei@outlook.com)'
