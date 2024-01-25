from .utils import generate_random_error
import random
from datetime import datetime


class PaymentService:
    """Класс-сервис для оплаты товаров"""

    def __init__(self):
        self.errors = generate_random_error()

    def pay_for_the_specified_order(self, request):
        """Метод для оплаты указанного заказа"""

        card_number = request.POST.get('numero1').replace(' ', '')
        order = request.user.order
        zero = '0'
        if int(card_number) % 2 == 0 and card_number[-1] != zero:
            order.status = 'paid'
            order.history_user = request.user
            order.payment_date = datetime.now()
            flag = True
        else:
            indexes = len(self.errors) - 1
            error_message = self.errors[random.randint(0, indexes)]
            order.error_message = error_message
            order.status = 'error'
            flag = False

        order.save()
        return flag

    def get_status_order(self):
        """Метод для получения статуса заказа"""
        pass