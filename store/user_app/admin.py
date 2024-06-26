from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'history_user', 'archived']
    list_display_links = ['pk', 'user', 'history_user']


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['phone', 'is_store']}), )
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ['phone', 'is_store', 'email']}), )
