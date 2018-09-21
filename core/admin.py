from django.contrib import admin

from .models import UserLoginActivity


class UserLoginActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserLoginActivity, UserLoginActivityAdmin)

