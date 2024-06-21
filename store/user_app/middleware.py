from django.urls import reverse


class CheckPathMiddleware:
    """Middleware для удаления данных из сессии, если пользователь прерывает регистрацию своего магазина на сайте"""

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.session.get('owner_data') is not None and request.path not in (
                reverse('user_app:register_seller_step_one'),
                reverse('user_app:register_seller_step_two')
        ):
            del request.session['owner_data']

        return self._get_response(request)
