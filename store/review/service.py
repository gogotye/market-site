from django.db.models import Count
from review.models import Review
from goods.models import Product


class ReviewsService:
    """Класс-сервис для работы с отзывами к товару"""

    @staticmethod
    def add_review_to_product(request) -> None:
        """Метод для добавления отзыва к товару"""

        review_text = request.POST.get('comment')
        user = request.user
        product = Product.objects.get(slug=request.POST.get('product_ind'))
        Review.objects.create(user=user, comment=review_text, product=product)


    @staticmethod
    def get_list_of_products_reviews(obj: Product, context: dict) -> None:
        """Метод для получения списка отзывов к товару"""

        reviews = obj.product_reviews.all().select_related('user')
        context.update({'reviews': reviews})


    def get_discount_on_cart(self):
        """Метод для получения скидки к корзине"""
        pass


    @staticmethod
    def get_number_of_reviews_for_product(obj: Product, context: dict) -> None:
        """Метод для получения количества отзывов к товару"""

        total = Product.objects.filter(pk=obj.pk).aggregate(total=Count('product_reviews'))
        context.update({'total': total.get('total')})