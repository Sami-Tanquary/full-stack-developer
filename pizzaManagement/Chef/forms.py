from django import forms
from Owner.models import Pizza


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple  # Use checkboxes for selecting toppings
        }