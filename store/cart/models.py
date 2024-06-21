from django.contrib.auth import get_user_model
from django.db import models


class Basket(models.Model):
    """Модель для хранения данных корзины пользователя"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey('goods.ProductShopRelations', on_delete=models.CASCADE, related_name='basket_products')
    quantity = models.SmallIntegerField(default=0, verbose_name='Количество')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    archived = models.BooleanField(default=False, verbose_name='Архивировано/Куплено')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
