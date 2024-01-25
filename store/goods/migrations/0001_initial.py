# Generated by Django 4.1.7 on 2023-04-13 12:25

from django.db import migrations, models
from my_store_app.utils import GetUploadPath


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название категории')),
                ('image', models.ImageField(blank=True, help_text='Необязательно.', upload_to=GetUploadPath.get_upload_path_for_category_image, verbose_name='Картинка категории')),
                ('slug', models.SlugField(help_text='Не рекомендуется изменять это поле самостоятельно.', max_length=150, unique=True, verbose_name='Название категории на латинице')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]