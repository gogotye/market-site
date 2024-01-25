from django.db.models import F, Sum
from django.http import HttpRequest
from .models import Basket
from django.conf import settings
from goods.models import ProductShopRelations
from django.db.models import DecimalField
from my_store_app.utils import round_total_sum
from django.conf import settings


class CartService:
    """Класс-сервис для манипуляции данным в корзине"""

    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_ID, {})
        if not cart:
            self.session[settings.CART_ID] = cart
        self.cart = cart

    def add_product_to_cart(self, product_shop: ProductShopRelations, request, quantity=1):
        """Метод для добавления товара в корзину"""

        if request.user.is_authenticated:
            cart = Basket.objects.get_or_create(user=request.user, product=product_shop, archived=False)
            self.change_quantity_of_products_in_cart(obj=cart[0], quantity=quantity)
        else:
            tab_pk = str(product_shop.pk)
            if tab_pk not in self.cart:
                self.cart[tab_pk] = {
                    'slug_product': product_shop.product.slug,
                    'quantity': quantity,
                    'price': float(product_shop.price),
                }
            else:
                self.change_quantity_of_products_in_cart(key=tab_pk, quantity=quantity)
            self.save()

        self.change_quantity_of_product_in_shop_product_table(product_shop=product_shop, quantity=-quantity)


    def delete_product_from_cart(self, cart: Basket=None, key: str=None):
        """Метод для удаления товара из корзины"""
        if key:
            del self.cart[key]
            self.save()
        else:
            cart.delete()

    def change_quantity_of_products_in_cart(self, quantity, key=None, obj=None):
        """Метод для изменения кол-ва товара в корзине"""

        if obj is None:
            self.cart[key]['quantity'] += quantity
            if self.cart[key]['quantity'] == 0:
                self.delete_product_from_cart(key=key)
        else:
            obj.quantity = F('quantity') + quantity
            obj.save()
            obj.refresh_from_db()

            if obj.quantity == 0:
                self.delete_product_from_cart(cart=obj)

    @staticmethod
    def get_list_of_products_in_cart(request):
        """Метод для получения списка товаров в корзине"""

        if not request.user.is_authenticated:
            cart: dict = request.session.get(settings.CART_ID)
            list_of_products = ProductShopRelations.objects.filter(pk__in=cart.keys()).select_related('product', 'shop')
            for i in list_of_products:
                curr_cart_row = cart.get(str(i.pk))
                i.total = round(curr_cart_row.get('quantity') * curr_cart_row.get('price'), 2)
                i.quantity_in_cart = curr_cart_row.get('quantity')
        else:
            list_of_products = Basket.objects.filter(
                user=request.user, archived=False,
            ).annotate(
                total=Sum(F('product__price') * F('quantity'), output_field=DecimalField(decimal_places=2))
            ).select_related('product__product__category')
            round_total_sum(list_of_products=list_of_products, field='total')

        return list_of_products


    def get_quantity_of_products_in_cart(self, request, queryset=None):
        """Метод для получения количества товаров в корзине"""

        if queryset:
            return queryset.filter(user=request.user).aggregate(summa=Sum('quantity'))['summa']

        return sum([val['quantity'] for val in self.cart.values()])

    def save(self):
        """Сохранение сессии"""

        self.session[settings.CART_ID].update(self.cart)
        self.session.modified = True

    def get_total_sum(self, request, queryset=None):
        """Метод получения общей суммы корзины"""

        if queryset:
            return round(queryset.filter(user=request.user).aggregate(total_sum=Sum(F('quantity') * F('product__price')))['total_sum'], 2)

        return round(sum([val['quantity'] * val['price'] for val in self.cart.values()]), 2)

    @staticmethod
    def change_quantity_of_product_in_shop_product_table(product_shop: ProductShopRelations, quantity: int) -> None:
        """Метод для изменения кол-ва товара в ProductShopRelations"""

        product_shop.quantity = F('quantity') + quantity
        product_shop.save()


