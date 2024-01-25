from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from ordering.models import Order


class Command(BaseCommand):
    help = 'Добавление разрешений на оплату заказа'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Order)
        methods = ('online_card', 'someone_card')
        for i in methods:
            codename = f'order_payment_permission_{i}'
            name = f'Order Payment Permission by {i}'
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )

            self.stdout.write(f'Новый Permission для оплаты заказа посредством {i} успешно создан.', self.style.SUCCESS)
