from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_store = models.BooleanField(default=False, verbose_name='Владелец магазина')
    phone = models.CharField(max_length=30, unique=True, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
