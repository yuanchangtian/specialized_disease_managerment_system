from django.contrib import admin
from django.db import models
from app01.models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','email')

admin.site.register(User, UserAdmin)
