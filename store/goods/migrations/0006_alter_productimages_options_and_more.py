# Generated by Django 4.1.7 on 2023-04-22 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_productimages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimages',
            options={'verbose_name': 'Изображение продукта', 'verbose_name_plural': 'Изображения продукта'},
        ),
        migrations.AlterModelOptions(
            name='productshoprelations',
            options={'verbose_name': 'Продукты-Магазины', 'verbose_name_plural': 'Продукты-Магазины'},
        ),
        migrations.AlterModelOptions(
            name='specifications',
            options={'verbose_name': 'Спецификация', 'verbose_name_plural': 'Спецификации'},
        ),
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
    ]