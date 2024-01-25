from django.db import models
from django.urls import reverse

from my_store_app.utils import GetUploadPath


class CategoryProduct(models.Model):
    """Модель для хранения записей категорий товара"""

    title = models.CharField(max_length=50, verbose_name='Название категории')
    image = models.ImageField(upload_to=GetUploadPath.get_upload_path_for_category_image, blank=True,
                              verbose_name='Картинка категории', help_text='Необязательно.')
    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='Название категории на латинице',
                            help_text='Не рекомендуется изменять это поле самостоятельно.')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Specifications(models.Model):
    """Модель спецификации"""

    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'

    pass


class Tags(models.Model):
    """Тэги для товаров"""

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    pass


class Product(models.Model):
    """Модель для хранения информации о продукте"""

    customers = models.ManyToManyField('customers_sellers.Customer', verbose_name='Покупатели', null=True, blank=True)
    shops = models.ManyToManyField('customers_sellers.Shop', verbose_name='Магазины', through='ProductShopRelations')
    category = models.ForeignKey('goods.CategoryProduct', on_delete=models.CASCADE, verbose_name='Категория товара',
                                 related_name='cat_products')
    specifications = models.ForeignKey('goods.Specifications', on_delete=models.CASCADE,
                                       verbose_name='Спецификация товара', related_name='sp_products')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара', blank=True)
    purchase_count = models.IntegerField(default=0, verbose_name='счетчик покупок данного товара')
    product_seen = models.IntegerField(default=0, verbose_name='счетчик просмотров данного товара')
    tags = models.ManyToManyField('Tags', related_name='products_tag', verbose_name='Тэги')
    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='Название товара на латинице',
                            help_text='Не рекомендуется изменять это поле самостоятельно.')
    is_active = models.BooleanField(default=False, verbose_name='Готов к продажам')
    title_picture = models.ImageField(blank=True, upload_to=GetUploadPath.get_upload_path_for_title_product_image,
                                      verbose_name='Титульное изображение')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('details:product_details', kwargs={'slug': self.slug})


class ProductShopRelations(models.Model):
    """Промежуточная модель, которая используется моделями Shop и Product"""

    shop = models.ForeignKey('customers_sellers.Shop', on_delete=models.CASCADE, verbose_name='Магазин', related_name='shop_products')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар', related_name='products')
    quantity = models.IntegerField(default=0, verbose_name='Количество товара')
    free_delivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Цена товара')

    class Meta:
        verbose_name = 'Продукты-Магазины'
        verbose_name_plural = 'Продукты-Магазины'


class ProductImages(models.Model):
    """Модель для хранения изображений продукта"""

    product = models.ForeignKey('goods.Product', on_delete=models.CASCADE, related_name='pictures', verbose_name='Товар')
    image = models.ImageField(upload_to=GetUploadPath.get_upload_path_for_product_images, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'