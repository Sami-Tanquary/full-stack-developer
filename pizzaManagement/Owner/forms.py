from django import forms
from .models import Topping


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Topping.objects.filter(name=name).exists():
            raise forms.ValidationError("A topping with this name already exists.")
        return name

