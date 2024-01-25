from django.contrib.auth.models import User
from django.db import models
from .utils import validate_image, GetUploadPath


class UrlRoad(models.Model):
    """Модель для хранения всех url путей на сайте"""

    category = models.CharField(max_length=150)
    page = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=200, blank=True)
    http_method = models.CharField(max_length=50)
    url = models.URLField(max_length=255, unique=True)
    comment = models.TextField(default='--')


class SiteConfiguration(models.Model):
    logo_image = models.ImageField(upload_to='logo/', verbose_name='Картинка логотипа', blank=True)
    contact_number = models.CharField(max_length=20, verbose_name='Контактный телефон', blank=True)
    contact_email = models.EmailField(verbose_name='Контактный e-mail', blank=True)

    @classmethod
    def get_config(cls):
        cong, _ = cls.objects.get_or_create(id=1)
        return cong

    class Meta:
        verbose_name = 'Конфигурации сайта'
        verbose_name_plural = 'Конфигурации сайта'





