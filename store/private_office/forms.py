from django import forms
from customers_sellers.models import Profile
from my_store_app.utils import validate_image

class ChangeProfileInfoFormLeft(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'Profile-file form-input'}),
                              validators=[validate_image], label='Аватар')

    class Meta:
        model = Profile
        fields = ['avatar', 'name', 'family_name', 'surname']


class ChangeProfileInfoFormRight(forms.Form):
    phone = forms.CharField(label='Телефон', required=False)
    email = forms.EmailField(label='E-mail', required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль', required=False)
