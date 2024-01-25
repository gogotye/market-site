from django import forms


class UserRegisterForm(forms.Form):
    name = forms.CharField(required=False, help_text='имя пользователя',
                                widget=forms.TextInput(attrs={'class': 'user-input', 'placeholder': 'Имя(необязательно)'}))
    family_name = forms.CharField(required=False, help_text='фамилия пользователя',
                           widget=forms.TextInput(attrs={'class': 'user-input', 'placeholder': 'Фамилия(необязательно)'}))
    surname = forms.CharField(required=False, help_text='отчество пользователя',
                                  widget=forms.TextInput(attrs={'class': 'user-input', 'placeholder': 'Отчество(необязательно)'}))
    phone = forms.CharField(required=True, help_text='номер телефона',
                            widget=forms.TextInput(attrs={'class': 'user-input', 'placeholder': '*Телефон'}))
    email = forms.EmailField(required=True,  help_text='email',
                             widget=forms.TextInput(attrs={'class': 'user-input', 'placeholder': '*E-mail'}))
    login = forms.CharField(required=True, help_text='логин',
                            widget=forms.TextInput(attrs={'class': 'user-input', 'placeholder': '*Логин'}))
    password = forms.CharField(required=True, help_text='пароль',
                               widget=forms.PasswordInput(attrs={'class': 'user-input', 'placeholder': '*Пароль'}))


class FirstStepForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))