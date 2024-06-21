from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from cart.models import Basket
from django.contrib.auth import get_user_model


class Order(models.Model):

    STATUS_CHOICES = [
        ('not_paid', 'Не оплачено'),
        ('paid', 'Оплачен'),
        ('error', 'Ошибка'),
    ]

    PAY_METHOD_CHOICES = [
        ('online_card', 'Онлайн картой'),
        ('random_check', 'Онлайн со случайного чужого счета'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('common', 'Обычная доставка'),
        ('express', 'Экспресс-доставка'),
    ]

    name = models.CharField(max_length=50, verbose_name='Имя')
    family_name = models.CharField(max_length=50, verbose_name='Фамилия')
    surname = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Активный пользователь',
                                       related_name='order', blank=True, null=True, help_text='Пользователь, на котором в данный момент закреплён заказ')
    total_price = models.DecimalField(verbose_name='Общая сумма', max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=30, verbose_name='номер телефона')
    email = models.EmailField(verbose_name='email пользователя')
    delivery_method = models.CharField(verbose_name='Способ доставки', blank=True, max_length=100,
                                       choices=DELIVERY_METHOD_CHOICES)
    city = models.CharField(verbose_name='Город доставки', blank=True, max_length=100)
    address = models.CharField(verbose_name='Адрес доставки', blank=True, max_length=250)
    pay_method = models.CharField(blank=True, max_length=100, choices=PAY_METHOD_CHOICES, verbose_name='Метод оплаты')
    comment = models.CharField(blank=True, max_length=350, verbose_name='Комментарий к заказу')
    delivery_price = models.SmallIntegerField(default=0, verbose_name='Сумма на доставку')
    status = models.CharField(verbose_name='Статус заказа', choices=STATUS_CHOICES, max_length=100)
    error_message = models.CharField(verbose_name='Описание ошибки оплаты', max_length=250, blank=True)
    history_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Архивный пользователь',
                                     blank=True, null=True, related_name='history_order')
    payment_date = models.DateTimeField(blank=True, verbose_name='Дата оплаты заказа')
    basket_objects = models.ManyToManyField(blank=True, verbose_name='Корзина заказа', related_name='order', to=Basket)
    archived = models.BooleanField(default=False, verbose_name='Архивированно/Заказ выполнен')

    def get_absolute_url(self):
        return reverse('order:order_details', kwargs={'pk': self.id})

    def clean(self):
        if not self.archived and Order.objects.filter(models.Q(email=self.email) | models.Q(phone=self.phone), archived=False).exclude(id=self.pk).exists():
            raise ValidationError('Активный заказ с таким номером телефона или email-почтой уже существует.')

