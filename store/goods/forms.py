from django import forms
from .models import Product


class FormProductAdmin(forms.ModelForm):
    title_pic = forms.ImageField(required=False,
                                 help_text='Изображение, которое будет показываться на карточке продукта.')
    pictures = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        help_text='Выберите одно или несколько неосновных изображений для продукта.',
        required=False,
    )

    class Meta:
        model = Product
        exclude = ['id', 'title_picture']
