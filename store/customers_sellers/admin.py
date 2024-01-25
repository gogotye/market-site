import os
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Customer, Shop, ShopInfo


class ProfileInline(admin.StackedInline):
    model = Profile

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    """Модель для интеграции Profile в админ-панель сайта"""

    list_display = ['pk', 'phone', 'email', 'show_avatar', 'show_user']
    list_display_links = ['pk', 'phone']

    def show_avatar(self, obj: Profile):
        if obj.avatar:
            return format_html(f'<img src={obj.avatar.url} width="50" height="50">')
    show_avatar.short_description = 'Фотография'

    def show_user(self, obj: Profile):
        return obj.customer.user
    show_user.short_description = 'Пользователь'
    
    def save_model(self, request, obj, form, change):
        if 'avatar' in form.changed_data:
            try:
                path = settings.BASE_DIR.joinpath('media', form.initial['avatar'].name)
                os.remove(path)
            except:
                pass
            else:
                parent_path = path.parent
                try:
                    os.rmdir(parent_path)
                except OSError as e:
                    print(f'Ошибка удаления: {e}')

        super().save_model(request, obj, form, change)

@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    """Модель для интеграции Customer в админ-панель сайта"""

    inlines = [ProfileInline]
    list_display = ['pk']


class AdminShopInfoInline(admin.TabularInline):
    model = ShopInfo

@admin.register(Shop)
class AdminShop(admin.ModelAdmin):
    """Модель для интеграции Shop в админ-панель сайта"""

    inlines = [AdminShopInfoInline]
    list_display = ['pk']

@admin.register(ShopInfo)
class AdminShopInfo(admin.ModelAdmin):
    """Модель для интеграции Shop в админ-панель сайта"""

    list_display = ['pk']
