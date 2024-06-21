from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from .forms import CustomerRegisterForm, FirstSellerRegisterForm, SecondSellerRegisterForm, FirstStepForm
from customers_sellers.models import Profile, Customer, ShopInfo, Shop
from django.contrib.auth import login
from goods.models import ProductShopRelations
from cart.service import CartService
from .utils import validate_user_data


class Login(LoginView):
    """Вход в учетную запись"""

    template_name = 'user_app/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        login(self.request, form.get_user())

        # Слияние корзин
        session_cart = self.request.session.get('cart')
        if session_cart:
            service = CartService(request=self.request)
            product_shop = ProductShopRelations.objects.filter(pk__in=service.cart.keys())
            for item in product_shop:
                service.add_product_to_cart(product_shop=item, request=self.request, quantity=service.cart[str(item.id)]['quantity'])
        try:
            del self.request.session['cart']
        except:
            pass

        if 'log' in self.request.POST:
            return redirect(reverse('order:step_1'))

        return HttpResponseRedirect(self.get_success_url())


class AuthorLogoutView(LogoutView):
    """Выход из учетной записи"""
    next_page = reverse_lazy('index')


class RegisterCustomerView(View):
    """Представление для регистрации пользователей и магазинов"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        form = CustomerRegisterForm()
        return render(request, 'user_app/register.html', context={'form': form})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = CustomerRegisterForm(request.POST)
        phone = request.POST['phone'][3:].replace(')', '-')
        email, username = request.POST['email'], request.POST['login']
        user_model = get_user_model()

        validate_user_data(user=user_model, form=form, username=username, email=email, phone=phone)

        if 'password2' in request.POST:
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('password2')
            if not pass1 == pass2:
                request.session['error_password'] = request.POST
                url = reverse('order:step_1')
                return redirect(url)

        if form.is_valid():
            new_user = user_model.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                phone=phone,
                email=form.cleaned_data['email']
            )

            customer = Customer.objects.create(user=new_user)

            Profile.objects.create(
                customer=customer,
                name=form.cleaned_data['name'] if form.cleaned_data['name'] else Profile._meta.get_field('name').default,
                family_name=form.cleaned_data['family_name'] if form.cleaned_data['family_name'] else Profile._meta.get_field('family_name').default,
                surname=form.cleaned_data['surname'] if form.cleaned_data['surname'] else Profile._meta.get_field('surname').default,
            )

            if 'reg' in request.POST:
                url = reverse('order:step_1') + '#open_auth_modal'
                return redirect(url)

            return redirect('index')

        if 'reg' in request.POST:
            url = reverse('order:step_1') + '#open_auth_modal_already_exists'
            return redirect(url)

        return render(request, 'user_app/register.html', context={'form': form})


class FirstRegisterSellerView(View):
    """Представление для регистрации магазина и владельца этого магазина"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        # заполнение существующими данными, формы регистрации
        user_data = request.session.get('owner_data')
        if user_data is not None:
            form = FirstSellerRegisterForm(user_data)
        else:
            form = FirstSellerRegisterForm()

        return render(request, 'user_app/register_seller_first.html', context={'form': form})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = FirstSellerRegisterForm(request.POST)
        phone = request.POST['phone'][3:].replace(')', '-')
        email, username = request.POST['email'], request.POST['username']
        user = get_user_model()

        validate_user_data(user=user, form=form, username=username, email=email, phone=phone)

        if form.is_valid():
            # подготовка к созданию пользователя
            # занесение всех необходимых данных в сессию
            request.session['owner_data'] = form.cleaned_data

            return redirect('user_app:register_seller_step_two')

        return render(request, 'user_app/register_seller_first.html', context={'form': form})


class SecondRegisterSellerView(View):
    """Представление для регистрации магазина и владельца этого магазина"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated or not request.session.get('owner_data'):
            return redirect('index')

        form = SecondSellerRegisterForm()
        return render(request, 'user_app/register_seller_second.html', context={'form': form})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = SecondSellerRegisterForm(request.POST)

        if form.is_valid():
            d = request.session['owner_data']

            # создание пользователя из данных сессии
            owner_user = get_user_model().objects.create_user(
                username=d['username'],
                password=d['password'],
                email=d['email'],
                phone=d['phone']
            )

            # привязка магазина к владельцу
            shop = Shop.objects.create(owner=owner_user)

            # привязка дополнительной информации к магазину
            ShopInfo.objects.create(
                shop=shop,
                owner_name=d['owner_name'] if d['owner_name'] else ShopInfo._meta.get_field('owner_name').default,
                owner_family_name=d['owner_family_name'] if d['owner_family_name'] else ShopInfo._meta.get_field('owner_family_name').default,
                owner_surname=d['owner_surname'] if d['owner_surname'] else ShopInfo._meta.get_field('owner_surname').default,
                **form.cleaned_data
            )

            return redirect('index')

        return render(request, 'user_app/register_seller_first.html', context={'form': form})


class RestorePasswordFirstStep(View):
    """Класс для сброса пароля"""

    def get(self, request):

        context = {
            'form': FirstStepForm()
        }

        return render(request, 'user_app/password-first-step.html', context=context)

    def post(self, request):
        form = FirstStepForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(customer__profile__email=form.cleaned_data['email']).first()
            if not user:
                messages.add_message(request=request, level=messages.WARNING, message='Пользователя с такой почтой не существует. Попробуйте ещё раз.')
                return render(request, 'user_app/password-first-step.html', context={'form': form})

            request.session['user_identifier'] = user.id
            return redirect('user_app:password_second')

        return render(request, 'user_app/password-first-step.html', context={'form': form})


class RestorePasswordSecondStep(View):
    def get(self, request):
        if not request.session.get('user_identifier'):
            messages.add_message(request=request, level=messages.WARNING, message='Сначала укажите почту для восстановления пароля')
            return render(request, 'user_app/password-first-step.html', context={'form': FirstStepForm()})

        return render(request, 'user_app/password-second-step.html')

    def post(self, request):
        if not request.session.get('user_identifier'):
            return self.get(request=request)

        id_user = request.session.get('user_identifier')
        user = User.objects.get(id=id_user)
        raw_password = request.POST.get('pass')
        if not raw_password:
            messages.add_message(request, messages.WARNING, 'Введите пароль!')
            return self.get(request=request)

        user.set_password(raw_password=raw_password)
        user.save()

        try:
            del request.session['user_identifier']
        except:
            pass

        return redirect('user_app:login')