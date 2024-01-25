from django.contrib import admin
from .models import SiteConfiguration
from django.conf import settings
import os


@admin.register(SiteConfiguration)
class AdminSiteConfiguration(admin.ModelAdmin):

    def has_add_permission(self, request):
        if SiteConfiguration.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if 'logo_image' in form.changed_data:
            try:
                path = settings.BASE_DIR.joinpath('media', form.initial['logo_image'].name)
                os.remove(path)
            except:
                pass
        obj.save()
