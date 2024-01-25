from customers_sellers.utils import remove_previous_image
from django.contrib import messages
from django.contrib.auth import decorators
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView
from customers_sellers.models import Profile
from ordering.models import Order
from .forms import ChangeProfileInfoFormLeft, ChangeProfileInfoFormRight
from my_store_app.utils import total_sum_and_quantity_update_context
from cart.service import CartService
from django.contrib.auth.mixins import LoginRequiredMixin



@decorators.login_required
def office(request):
    cart_service = CartService(request=request)
    queryset = cart_service.get_list_of_products_in_cart(request=request)
    user = request.user

    flag_for_payment = order_continue_flag = False
    if hasattr(user, 'order'):
        order = user.order
        if order.error_message:
            flag_for_payment = True
        elif order.status == 'not_paid':
            order_continue_flag = True
    else:
        # Если активного заказа у пользователя нет, то выбирается последний(по дате оплаты) заказ и отображается в личном кабинете
        order = Order.objects.filter(history_user=user, user__isnull=True).order_by('-payment_date').first()

    context = {
        'menu_item': 'Личный кабинет',
        'order': order,
        'flag_for_payment': flag_for_payment,
        'order_continue_flag': order_continue_flag,
    }

    if hasattr(user, 'customer'):
        user_profile = user.customer.profile
        user_profile_opts = user_profile._meta

        default_values_dict = {
            'name_default_value': user_profile_opts.get_field('name').default,
            'family_name_default_value': user_profile_opts.get_field('family_name').default,
            'surname_default_value': user_profile_opts.get_field('surname').default,
        }

        context.update(default_values_dict)

    total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

    return render(request, 'private_office/account.html', context)


@decorators.login_required
def profile(request: HttpRequest):
    cart_service = CartService(request=request)
    queryset = cart_service.get_list_of_products_in_cart(request=request)
    avatar = request.FILES.get('avatar')

    if request.method == 'POST':
        #POST запрос
        post_dict = request.POST.copy()
        post_dict['phone'] = post_dict.get('phone')[3:].replace(')', '-')

        form_left = ChangeProfileInfoFormLeft(post_dict, request.FILES)
        form_right = ChangeProfileInfoFormRight(post_dict)
        if form_left.is_valid() and form_right.is_valid():
            user: User = request.user

            profile_user = Profile.objects.filter(customer=user.customer).first()
            profile_user.name = form_left.cleaned_data['name']
            profile_user.family_name = form_left.cleaned_data['family_name']
            profile_user.surname = form_left.cleaned_data['surname']
            profile_user.phone = form_right.cleaned_data['phone']
            profile_user.email = form_right.cleaned_data['email']

            if avatar:
                remove_previous_image(media_path=profile_user.avatar.name)
                profile_user.avatar = avatar
            profile_user.save()

            messages.add_message(request=request, level=messages.SUCCESS,
                                 message='Данные профиля успешно сохранены.')

            if form_right.cleaned_data['password1']:
                first_pass = form_right.cleaned_data['password1']
                second_pass = form_right.cleaned_data['password2']
                if first_pass == second_pass:
                    user.set_password(first_pass)
                    user.save()
                    messages.add_message(request=request, level=messages.SUCCESS,
                                         message='Пароль изменён успешно.')
                else:
                    form_right.add_error('password2', 'Пароли не совпадают')
                    messages.add_message(request=request, level=messages.WARNING,
                                         message='Пароль не был изменён.')

        context = {
            'menu_item': 'Профиль',
            'left_form': form_left,
            'right_form': form_right,
        }
        total_sum_and_quantity_update_context(context=context, request=request, queryset_for_cart_table=queryset)

        return render(request, 'private_office/profile.html', context)

    #GET запрос
    profile_inst = request.user.customer.profile
    profile_dict = model_to_dict(profile_inst, fields=['name', 'family_name', 'surname', 'phone', 'email', 'avatar'])
    context = {
        'menu_item': 'Профиль',
        'left_form': ChangeProfileInfoFormLeft(profile_dict),
        'right_form': ChangeProfileInfoFormRight(profile_dict)
    }
    total_sum_and_quantity_update_context(request=request, context=context, queryset_for_cart_table=queryset)

    return render(request, 'private_office/profile.html', context)


class HistoryView(LoginRequiredMixin, ListView):
    template_name = 'private_office/historyorder.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user__isnull=True, history_user=self.request.user).order_by('-payment_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        cart_service = CartService(request=self.request)
        context = super().get_context_data(object_list=None, **kwargs)
        context['menu_item'] = 'История заказов'
        total_sum_and_quantity_update_context(
            context=context,
            request=self.request,
            queryset_for_cart_table=cart_service.get_list_of_products_in_cart(request=self.request)
        )
        return context


@decorators.login_required
def delete_avatar(request: HttpRequest):
    profile_obj = request.user.customer.profile
    if profile_obj.avatar:
        remove_previous_image(profile_obj.avatar.name)
        profile_obj.avatar = ''
        profile_obj.save()
        messages.add_message(request=request, level=messages.SUCCESS, message='Аватар успешно удалён!')
    return redirect('private_office:profile')