from django import forms
from .models import Topping


# Class: ToppingForm
# Description: Form for adding or updating toppings.
class ToppingForm(forms.ModelForm):
    # Metaclass to specify model and fields
    class Meta:
        # Model associated with the form
        model = Topping
        # Fields to include in the form (the topping name)
        fields = ['name']

    # Function: clean_name
    # Parameters: self
    # Description: Validates the name field to ensure uniqueness of topping names.
    # Returns: The cleaned name if it's unique.
    def clean_name(self):
        # Get the cleaned name from the form data
        name = self.cleaned_data.get('name')
        if name:
            # Strip leading and trailing whitespaces from the name field
            name = name.strip()
        # Get the instance of the form, if it exists
        instance = getattr(self, 'instance', None)
        # Check if an instance exists and if a topping with the same name already exists
        if instance and Topping.objects.exclude(pk=instance.pk).filter(name__iexact=name).exists():
            # Raise a validation error if a topping with the same name already exists
            raise forms.ValidationError("A topping with this name already exists.")
        # Return the cleaned name if it's unique
        return name

