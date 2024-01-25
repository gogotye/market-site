from datetime import datetime
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.db import IntegrityError
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from cart.models import Basket
from cart.service import CartService
from customers_sellers.models import Profile
from my_store_app.utils import total_sum_and_quantity_update_context
from .forms import OrderStep1FormIfNotLogin, OrderStep1Form, DeliveryAddressForm, PayMethodForm
from .models import Order
from .utils import add_order_step_permission_to_user, delete_permissions
from django.forms.models import model_to_dict
from .forms import CommentForm
from .service import PaymentService


class OrderViewStep1(View):
    def get(self, request, **kwargs):
        cart_service = CartService(request=request)


        queryset = cart_service.get_list_of_products_in_cart(request=request)
        if not queryset:
            url = reverse('cart:cart') + '#empty_basket'
            return redirect(url)
        elif not isinstance(queryset.first(), Basket):
            queryset = None

        if 'non_field_error_name' in kwargs:
            user_form = kwargs['non_field_error_name']
        elif request.user.is_authenticated and hasattr(request.user, 'order'):
            order = request.user.order
            #order_dict = model_to_dict(order, fields=['name', 'family_name', 'surname', 'phone', 'email'])
            user_form = OrderStep1Form(instance=order)
        elif request.user.is_authenticated:
            profile = request.user.customer.profile
            profile_dict = model_to_dict(profile, fields=['name', 'family_name', 'surname', 'phone', 'email'])
            user_form = OrderStep1Form(profile_dict)
        else:
            user_form = OrderStep1Form()

        if 'error_password' in request.session:
            auth_form = OrderStep1FormIfNotLogin(request.session['error_password'])
            auth_form.add_error('password', 'Пароли не совпадают')
            del request.session['error_password']
        else:
            auth_form = OrderStep1FormIfNotLogin()

        context = {
            'step': 1,
            'auth_form': auth_form,
            'user_form': user_form,
            'login_form': AuthenticationForm(),
        }

        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'ordering/order_step_1.html', context=context)

    def post(self, request):
        values = request.POST.dict()
        values['phone'] = values.get('phone')[3:].replace(')', '-')

        form = OrderStep1Form(values, instance=request.user.order) if hasattr(request.user, 'order') else OrderStep1Form(values)

        if request.POST.get('name') == Profile._meta.get_field('name').default or request.POST.get('family_name') == Profile._meta.get_field('family_name').default:
            form.add_error(None, 'Нужно указать фамилию и имя!')

        if form.is_valid():
            total = round(Basket.objects.filter(user=request.user, archived=False).aggregate(total=Sum(F('product__price') * F('quantity')))['total'], 2)
            surname = '' if form.cleaned_data.get('surname') == Profile._meta.get_field('surname').default else form.cleaned_data.get('surname')
            if not Order.objects.filter(user=request.user, archived=False).exists():
                Order.objects.create(user=request.user, phone=form.cleaned_data.get('phone'),
                                     total_price=total, surname=surname,
                                     name=form.cleaned_data.get('name'),
                                     family_name=form.cleaned_data.get('family_name'),
                                     email=form.cleaned_data.get('email'),
                                     status='not_paid', payment_date=datetime.now())
            else:
                Order.objects.filter(user=request.user, archived=False).update(phone=form.cleaned_data.get('phone'), total_price=total,
                                                               surname=surname, name=form.cleaned_data.get('name'),
                                                               family_name=form.cleaned_data.get('family_name'),
                                                               email=form.cleaned_data.get('email'),
                                                               status='not_paid', payment_date=datetime.now())

            # Добавление разрешения на продолжение оформления заказа
            add_order_step_permission_to_user(request=request, codename='step_order_permission_2')

            return redirect(reverse('order:step_2'))

        return self.get(request, non_field_error_name=form)




class OrderViewStep2(PermissionRequiredMixin, View):
    permission_required = 'ordering.step_order_permission_2'

    def get(self, request):
        cart_service = CartService(request=request)

        order = request.user.order
        delivery_dict = model_to_dict(order, fields=['address', 'city'])

        context = {
            'step': 2,
            'form': DeliveryAddressForm(delivery_dict),
        }
        queryset = cart_service.get_list_of_products_in_cart(request=request)
        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'ordering/order_step_2.html', context=context)


    def post(self, request):
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            order = request.user.order

            if order.delivery_price:
                order.total_price -= order.delivery_price
                order.save()

            delivery_method = request.POST.get('delivery')
            if delivery_method == 'common':
                if order.total_price < settings.FREE_DELIVERY_BORDER:
                    order.total_price += settings.COMMON_DELIVERY_PRICE
                    order.delivery_price = settings.COMMON_DELIVERY_PRICE
                order.delivery_method = delivery_method
            elif delivery_method == 'express':
                order.total_price += settings.EXPRESS_DELIVERY_PRICE
                order.delivery_method = delivery_method
                order.delivery_price = settings.EXPRESS_DELIVERY_PRICE
            else:
                return self.get(request=request)

            order.city = request.POST.get('city')
            order.address = request.POST.get('address')
            order.save()

            # Добавление разрешения на продолжение оформления заказа
            add_order_step_permission_to_user(request=request, codename='step_order_permission_3')

            return redirect(reverse('order:step_3'))

        return self.get(request=request)


class OrderViewStep3(PermissionRequiredMixin, View):
    permission_required = 'ordering.step_order_permission_3'

    def get(self, request):
        cart_service = CartService(request=request)

        context = {
            'step': 3,
            'form': PayMethodForm(),
        }
        queryset = cart_service.get_list_of_products_in_cart(request=request)
        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'ordering/order_step_3.html', context=context)

    def post(self, request):
        order = request.user.order
        form = PayMethodForm(request.POST)
        if form.is_valid():
            pay_method = request.POST.get('pay')
            if pay_method == 'online_card':
                order.pay_method = pay_method
            elif pay_method == 'random_check':
                order.pay_method = pay_method
            else:
                return self.get(request=request)

            order.save()

            # Добавление разрешения на продолжение оформления заказа
            add_order_step_permission_to_user(request=request, codename='step_order_permission_4')

            return redirect(reverse('order:step_4'))

        return self.get(request=request)


class OrderViewStep4(PermissionRequiredMixin, View):
    permission_required = 'ordering.step_order_permission_4'

    def get(self, request, **kwargs):
        cart_service = CartService(request=request)

        if 'comment_error' in kwargs:
            comment_form = kwargs['comment_error']
        else:
            comment_form = CommentForm()

        queryset = cart_service.get_list_of_products_in_cart(request=request)
        context = {
            'step': 4,
            'order': request.user.order,
            'basket': queryset,
            'comment_form': comment_form,
        }
        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'ordering/order_step_4.html', context=context)

    def post(self, request):
        if 'comment' in request.POST:
            comment = request.POST.get('comment')
            form = CommentForm(request.POST)
            if form.is_valid():
                order = request.user.order
                order.comment = comment
                order.save()
                return self.get(request=request)
            return self.get(request=request, comment_error=form)
        elif 'payment' in request.POST:
            order = request.user.order
            codename_online_card = 'order_payment_permission_online_card'
            codename_someone_card = 'order_payment_permission_someone_card'

            # Добавление разрешения на оплату заказа и удаления (если существует) другого разрешения на оплату
            if order.pay_method == 'online_card':
                add_order_step_permission_to_user(request=request, codename=codename_online_card)
                del_perm = Permission.objects.get(codename=codename_someone_card)

                if request.user.user_permissions.filter(id=del_perm.id).exists():
                    request.user.user_permissions.remove(del_perm)
                return redirect('order:payment_online')

            else:
                add_order_step_permission_to_user(request=request, codename=codename_someone_card)
                del_perm = Permission.objects.get(codename=codename_online_card)

                if request.user.user_permissions.filter(id=del_perm.id).exists():
                    request.user.user_permissions.remove(del_perm)
                return redirect('order:payment_someone')

        return self.get(request=request)


class PaymentOnlineCardView(PermissionRequiredMixin, View, PaymentService):
    permission_required = 'ordering.order_payment_permission_online_card'

    def __init__(self):
        super().__init__()
        PaymentService.__init__(self)

    def get(self, request, **kwargs):
        cart_service = CartService(request=request)

        queryset = cart_service.get_list_of_products_in_cart(request=request)
        context = {
            'basket': queryset,
        }
        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'ordering/payment.html', context=context)

    def post(self, request):
        # оплата
        list_of_permissions = [f'order_payment_permission_{i}' for i in ('online_card', 'someone_card')]

        if self.pay_for_the_specified_order(request=request):
            order_to_update = request.user.order
            cart = Basket.objects.filter(user=request.user, archived=False)
            for obj in cart:
                order_to_update.basket_objects.add(obj)

            order_to_update.user = None
            order_to_update.archived = True

            if order_to_update.error_message:
                order_to_update.error_message = ''
            order_to_update.save()
            cart.update(archived=True)

            # Удаление всех permissions для оплаты и прохождения шагов для оформления заказа
            list_of_permissions.extend([f'step_order_permission_{i}' for i in range(2, 5)])
            delete_permissions(request=request, permissions=list_of_permissions)
        else:
            # Удаление permissions для оплаты
            delete_permissions(request=request, permissions=list_of_permissions)

        url = reverse('index') + '#order'
        return redirect(url)


class PaymentSomeoneCardView(PaymentOnlineCardView):
    permission_required = 'ordering.order_payment_permission_someone_card'

    def get(self, request, **kwargs):
        cart_service = CartService(request=request)

        queryset = cart_service.get_list_of_products_in_cart(request=request)
        context = {
            'basket': queryset,
        }
        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'ordering/paymentsomeone.html', context=context)


class OrderDetails(DetailView):
    model = Order
    template_name = 'ordering/oneorder.html'
    context_object_name = 'order'