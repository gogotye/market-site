# Generated by Django 4.1.7 on 2023-04-13 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_specifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]