from django.shortcuts import render, redirect
from django.views import View
from my_store_app.utils import total_sum_and_quantity_update_context
from .models import Basket
from .service import CartService
from goods.models import ProductShopRelations


class CartView(View):
    """Представление для отображения корзины"""


    def get(self, request, *args, **kwargs):
        cart_service = CartService(request=request)

        context = {
            'basket': cart_service.get_list_of_products_in_cart(request=request)
        }

        if request.user.is_authenticated:
            queryset = context['basket']
        else:
            queryset = None

        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'cart/cart.html', context=context)


    def post(self, request, *args, **kwargs):
        cart_service = CartService(request=request)
        pr_id = request.POST.get('add') or request.POST.get('remove') or request.POST.get('delete_cart_row')

        if request.POST.get('add') or request.POST.get('remove'):
            cart_product_shop = Basket.objects.filter(pk=pr_id).select_related('product').first().product if request.user.is_authenticated else ProductShopRelations.objects.get(pk=pr_id)
            quantity = 1 if 'add' in request.POST else -1
            cart_service.add_product_to_cart(product_shop=cart_product_shop, request=request, quantity=quantity)

        elif request.POST.get('delete_cart_row'):
            cart_to_delete = Basket.objects.filter(pk=pr_id).select_related('product').first() if request.user.is_authenticated else ProductShopRelations.objects.get(pk=pr_id)
            product_shop = cart_to_delete.product if isinstance(cart_to_delete, Basket) else cart_to_delete
            quantity = cart_to_delete.quantity if isinstance(cart_to_delete, Basket) else cart_service.cart[pr_id].get('quantity')
            cart_service.change_quantity_of_product_in_shop_product_table(product_shop=product_shop, quantity=quantity)
            cart_service.delete_product_from_cart(key=pr_id)

        return redirect('cart:cart')
