from django.db.models import Q, Avg
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from goods.models import Product
from customers_sellers.models import Shop
from my_store_app.utils import sort_by
from cart.service import CartService
from my_store_app.utils import total_sum_and_quantity_update_context, get_product_shop_with_min_price, round_total_sum
from .forms import NameForm


class CatalogView(ListView):
    """Представление для отображения каталога"""

    paginate_by = 3
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_active=True).annotate(avg_price=Avg('products__price'))

    def get_queryset(self):
        result = super().get_queryset()
        category_selected = self.request.GET.get('category')

        filtered = self.request.session.get('filtered', {}).get('filtered')
        if category_selected and filtered:
            result = result.filter(category__slug=category_selected, id__in=filtered)
        elif filtered:
            result = result.filter(id__in=filtered)
        elif category_selected:
            result = result.filter(category__slug=category_selected)

        sorting = self.request.GET.get('sort_by')
        if sorting:
            result = sort_by(queryset=result, request=self.request, key=sorting)

        round_total_sum(list_of_products=result, field='avg_price')
        return result


    def get_context_data(self, *, object_list=None, **kwargs):
        res = super().get_context_data(object_list=None, **kwargs)

        res['shop_list'] = Shop.objects.all()
        total_sum_and_quantity_update_context(context=res, request=self.request)

        user_search = self.request.session.get('filtered', {}).get('user_input')
        if user_search:
            res['name_form'] = NameForm({'title': user_search})
        else:
            res['name_form'] = NameForm()

        return res


    def post(self, request: HttpRequest, *args, **kwargs):
        if request.POST.get('clear') and 'filtered' in self.request.session:
            del self.request.session['filtered']
            return redirect('catalog:catalog')

        elif request.POST.get('price'):
            lowest_price, highest_price = map(float, request.POST.get('price').split(';'))
            products = super().get_queryset().filter(Q(products__price__gte=lowest_price) & Q(products__price__lte=highest_price))

            selected_shops = request.POST.getlist('selected_shops')

            request.session['filtered'] = dict()

            if request.POST.get('title'):
                products = products.filter(Q(title__iregex=request.POST.get('title')) | Q(description__iregex=request.POST.get('title')))
                request.session['filtered']['user_input'] = request.POST.get('title')
            if request.POST.get('free'):
                products = products.filter(products__free_delivery=True)
            if request.POST.get('in_stock'):
                products = products.filter(products__quantity__gt=0)
            if selected_shops:
                products = products.filter(shops__shop_info__name__in=selected_shops)

            new_lst = [elem.pk for elem in products]

            request.session['filtered'].update({'filtered': new_lst, 'min': int(lowest_price), 'max': int(highest_price)})

            if 'category' in request.GET:
                url = reverse('catalog:catalog') + f'?category={request.GET["category"]}'
                return redirect(url)
            return redirect('catalog:catalog')

        elif request.POST.get('product'):
            cart_service = CartService(request=request)
            product_shop = get_product_shop_with_min_price(request=request)

            cart_service.add_product_to_cart(product_shop=product_shop, request=request)
            return self.get(request, *args, **kwargs)

