from django import forms
from ordering.models import Order


class OrderStep1Form(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'family_name', 'surname', 'phone', 'email']


class OrderStep1FormIfNotLogin(forms.Form):
    login = forms.CharField(label='Имя пользователя', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль', required=True)


class DeliveryAddressForm(forms.Form):
    MY_CHOICES = [
        ('common', 'Обычная доставка'),
        ('express', 'Экспресс-доставка'),
    ]

    delivery = forms.CharField(widget=forms.RadioSelect(choices=MY_CHOICES))
    city = forms.CharField(max_length=100, label='Город', widget=forms.TextInput(attrs={'class': 'form-input'}))
    address = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 1, 'cols': 15}), label='Адрес')


class PayMethodForm(forms.Form):
    MY_CHOICES = [
        ('online_card', 'Онлайн картой'),
        ('random_check', 'Онлайн со случайного чужого счета'),
    ]

    pay = forms.CharField(widget=forms.RadioSelect(choices=MY_CHOICES))


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=350, label='Комментарий к заказу', widget=forms.Textarea(attrs={'class': 'full', 'rows': 4}))
