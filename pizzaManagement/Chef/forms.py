from django import forms
from Owner.models import Pizza


# Class: PizzaForm
# Description: Form class for creating and updating Pizza objects.
# Parameters:
#   - forms.ModelForm: The base class for the form, provided by Django.
class PizzaForm(forms.ModelForm):
    # Metaclass to define metadata for the form
    class Meta:
        # Use the Pizza model
        model = Pizza
        # Specify the fields to include in the form (name, toppings)
        fields = ['name', 'toppings', 'crust']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple # Use checkboxes for selecting toppings
        }

    # Function: clean_name
    # Parameters: self
    # Description: Custom form validation method to ensure uniqueness of pizza names.
    # Returns: The cleaned pizza name if it's unique; otherwise, raises a ValidationError.
    def clean_name(self):
        # Get the cleaned pizza name from form data
        name = self.cleaned_data.get('name')
        if name:
            # Strip leading and trailing whitespaces from the name field
            name = name.strip()
        # Get the instance of the form (if any)
        instance = getattr(self, 'instance', None)
        # Check if an instance exists and if a pizza with the same name already exists (excluding the current instance)
        if instance and Pizza.objects.exclude(pk=instance.pk).filter(name__iexact=name).exists():
            # Raise a ValidationError if a pizza with the same name already exists
            raise forms.ValidationError("A pizza with this name already exists.")
        # Return the cleaned pizza name if it's unique
        return name
