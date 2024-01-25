from django.contrib.auth.models import Permission
from string import ascii_letters, digits, whitespace
import random


def add_order_step_permission_to_user(request, codename):
    perm_name = f'ordering.{codename}'
    if not request.user.has_perm(perm_name):
        permission = Permission.objects.get(codename=codename)
        request.user.user_permissions.add(permission)


def generate_random_error():
    number_of_errors = 20
    errors_list = []

    for i in range(number_of_errors):
        length = random.randint(10, 50)
        symbols = ascii_letters + digits + whitespace[0]
        symbols_max_index = len(symbols) - 1
        error_message = ''
        for _ in range(length):
            error_message += symbols[random.randint(0, symbols_max_index)]
        errors_list.append(error_message)

    return errors_list


def delete_permissions(request, permissions: list):
    user = request.user
    perms = Permission.objects.filter(codename__in=permissions)

    for obj in perms:
        user.user_permissions.remove(obj)
