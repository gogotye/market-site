from django.db.models import Avg
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from my_store_app.utils import get_active_categories, total_sum_and_quantity_update_context,\
    get_product_shop_with_min_price, round_total_sum
from goods.models import Product
from cart.service import CartService


class CategoryView(View):
    """Формирование списка категорий, популярных товаров,
         лимитированных, баннеров и путей до изображений этих категорий"""

    def get(self, request: HttpRequest):
        cart_service = CartService(request)

        popular_product = Product.objects.filter(
                is_active=True
            ).annotate(avg_price=Avg('products__price')).order_by('-purchase_count')[:8]
        round_total_sum(list_of_products=popular_product, field='avg_price')

        context = {
            'popular_product': popular_product,                                                     # 8 популярных продуктов
        }

        if request.user.is_authenticated:
            queryset = cart_service.get_list_of_products_in_cart(request=request)
        else:
            queryset = None

        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)       # Обновление context

        return render(request, 'index.html', context=context)

    def post(self, request: HttpRequest, *args, **kwargs):
        service = CartService(request)
        product_shop = get_product_shop_with_min_price(request=request)

        service.add_product_to_cart(product_shop=product_shop, request=request)
        return self.get(request)






