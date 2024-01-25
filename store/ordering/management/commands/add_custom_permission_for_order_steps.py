from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from ordering.models import Order


class Command(BaseCommand):
    help = 'Добавление новых Permission для прохождения шагов создания заказа'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Order)

        for i in range(2, 5):
            codename = f'step_order_permission_{i}'
            name = f'Step {i} Order Permission'
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )

            self.stdout.write(f'Новый Permission для шага {i} успешно создан.', self.style.SUCCESS)


