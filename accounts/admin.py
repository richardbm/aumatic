from django.contrib import admin
from accounts import models
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.User, UserAdmin)