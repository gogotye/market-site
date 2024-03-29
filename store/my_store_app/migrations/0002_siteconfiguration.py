                                                            # Generated by Django 4.1.7 on 2023-04-14 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_image', models.ImageField(blank=True, upload_to='logo/', verbose_name='Картинка логотипа')),
                ('contact_number', models.CharField(blank=True, max_length=20, verbose_name='Контактный телефон')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Контактный e-mail')),
            ],
            options={
                'verbose_name': 'Конфигурации сайта',
                'verbose_name_plural': 'Конфигурации сайта',
            },
        ),
    ]
