from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OTP

admin.site.register(OTP)
admin.site.register(User)

# @admin.register(User)
# class AppUserAdmin(UserAdmin):
#     pass