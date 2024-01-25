from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'history_user', 'archived']
    list_display_links = ['pk', 'user', 'history_user']


