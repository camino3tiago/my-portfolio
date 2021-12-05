from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Skill, Service

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

admin.site.unregister(Group)

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Service)