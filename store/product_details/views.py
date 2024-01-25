from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from goods.models import Product
from django.core.cache import cache
from django.conf import settings
from cart.service import CartService
from review.service import ReviewsService
from review.forms import FormReview
from my_store_app.utils import get_product_shop_with_min_price, total_sum_and_quantity_update_context, get_active_categories


class ProductDetails(DetailView, ReviewsService):
    model = Product
    template_name = 'product_details/product.html'
    context_object_name = 'details'
    extra_context = {'form': FormReview()}

    def get_object(self, queryset=None):
        key = f'product_details_{self.kwargs.get("slug")}'
        if cache.get(key) is None:
            result = super().get_object()
            cache.set(key, result, settings.CACHE_TTL)

        result = cache.get(key)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_number_of_reviews_for_product(obj=self.get_object(), context=context)
        self.get_list_of_products_reviews(obj=self.get_object(), context=context)
        total_sum_and_quantity_update_context(context=context, request=self.request)
        get_active_categories(context=context)
        return context

    def post(self, request, *args, **kwargs):
        cart_service = CartService(request=request)

        if request.POST.get('amount'):
            quantity_to_add = request.POST.get('amount')
            lowest_price_product = get_product_shop_with_min_price(request=request)
            cart_service.add_product_to_cart(product_shop=lowest_price_product, request=request, quantity=quantity_to_add)

        elif request.POST.get('comment'):
            self.add_review_to_product(request=request)
            url = reverse('details:product_details', kwargs={'slug': self.kwargs.get('slug')})
            return redirect(url)

        return self.get(request, *args, **kwargs)

