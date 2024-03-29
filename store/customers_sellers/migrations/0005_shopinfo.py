# Generated by Django 4.1.7 on 2023-04-14 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers_sellers', '0004_customer_products_shop_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_info', to='customers_sellers.shop', verbose_name='Магазин')),
                ('name', models.CharField(max_length=250, verbose_name='Название магазина')),
            ],
        ),
    ]
