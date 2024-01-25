from django import forms


class NameForm(forms.Form):
    title = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-input form-input_full', 'id': 'title', 'placeholder': 'Название'}
        )
    )