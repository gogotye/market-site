from django.db import models
from django.contrib.auth import get_user_model


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('goods.Product', on_delete=models.CASCADE, related_name='product_reviews')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
