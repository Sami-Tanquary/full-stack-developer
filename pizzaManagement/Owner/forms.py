from django import forms
from .models import Topping


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name']