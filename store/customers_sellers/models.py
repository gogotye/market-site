from django.contrib.auth.models import User
from django.db import models
from my_store_app.utils import GetUploadPath, validate_image


class Profile(models.Model):
    """Модель для хранения информации о пользователе на сайте"""

    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(default='Имя не указано', max_length=50, verbose_name='Имя', help_text='Необязательно')
    family_name = models.CharField(default='Фамилия не указана', max_length=50, verbose_name='Фамилия', help_text='Необязательно')
    surname = models.CharField(default='Отчество не указано', max_length=50, verbose_name='Отчество', help_text='Необязательно')
    phone = models.CharField(max_length=30, verbose_name='номер телефона', unique=True)
    email = models.EmailField(verbose_name='email пользователя', unique=True)
    avatar = models.ImageField(upload_to=GetUploadPath.get_upload_path_for_user_avatar, blank=True,
                               validators=[validate_image], help_text='Необязательно.')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'


class Customer(models.Model):
    """Модель для хранения информации для покупателя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='customer')
    products = models.ManyToManyField('goods.Product', verbose_name='Продукты', blank=True, null=True)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Shop(models.Model):
    """Модель для хранения информации о магазине"""

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец', related_name='shop')
    products = models.ManyToManyField('goods.Product', verbose_name='Продукты', through='goods.ProductShopRelations')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class ShopInfo(models.Model):
    """Модель для хранения дополнительной информации о магазине"""

    name = models.CharField(max_length=250, verbose_name='Название магазина')
    shop = models.OneToOneField('Shop', on_delete=models.CASCADE, verbose_name='Магазин', related_name='shop_info')

    class Meta:
        verbose_name = 'Информация о магазине'
        verbose_name_plural = 'Информация о магазинах'
