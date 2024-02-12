from django import forms
from Owner.models import Pizza


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple  # Use checkboxes for selecting toppings
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        instance = getattr(self, 'instance', None)
        if instance and Pizza.objects.exclude(pk=instance.pk).filter(name=name).exists():
            raise forms.ValidationError("A pizza with this name already exists.")
        return name
