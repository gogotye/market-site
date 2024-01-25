from django import forms

class FormReview(forms.Form):
    comment = forms.CharField(max_length=2000, required=True,
                              widget=forms.Textarea(attrs={"class": "form-textarea", "placeholder": "Отзыв"}))