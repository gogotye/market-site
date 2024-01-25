from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.reverse import reverse
from .forms import UserRegisterForm, FirstStepForm
from customers_sellers.models import Profile, Customer
from django.contrib.auth import login
from goods.models import ProductShopRelations
from cart.service import CartService



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


class RegisterView(View):
    """Представление для регистрации пользователей и магазинов"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        form = UserRegisterForm()
        return render(request, 'user_app/register.html', context={'form': form})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        phone = request.POST['phone'][3:].replace(')', '-')
        email = request.POST['email']
        username = request.POST['login']

        if User.objects.filter(username=username).exists():
            form.add_error('login', 'Пользователь с таким логином уже существует.')
        elif Profile.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с таким e-mail уже существует.')
        elif Profile.objects.filter(phone=phone).exists():
            form.add_error('phone', 'Пользователь с таким телефоном уже существует.')

        if 'password2' in request.POST:
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('password2')
            if not pass1 == pass2:
                request.session['error_password'] = request.POST
                url = reverse('order:step_1')
                return redirect(url)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            phone = form.cleaned_data['phone'][3:].replace(')', '-')
            customer = Customer.objects.create(user=user)

            Profile.objects.create(
                customer=customer,
                name=form.cleaned_data['name'] if form.cleaned_data['name'] else Profile._meta.get_field('name').default,
                family_name=form.cleaned_data['family_name'] if form.cleaned_data['family_name'] else Profile._meta.get_field('family_name').default,
                surname=form.cleaned_data['surname'] if form.cleaned_data['surname'] else Profile._meta.get_field('surname').default,
                phone=phone,
                email=form.cleaned_data['email']
            )

            if 'reg' in request.POST:
                url = reverse('order:step_1') + '#open_auth_modal'
                return redirect(url)

            return redirect('index')

        if 'reg' in request.POST:
            url = reverse('order:step_1') + '#open_auth_modal_already_exists'
            return redirect(url)

        return render(request, 'user_app/register.html', context={'form': form})


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