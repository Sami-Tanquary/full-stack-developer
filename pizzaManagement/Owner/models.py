from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower


# Class: Topping
# Description: Model representing a pizza topping.
class Topping(models.Model):
    # Name of the topping, should be unique
    name = models.CharField(max_length=100, unique=True, blank=False, null=False, db_index=True)

    class Meta:
        ordering = [Lower('name')]  # Case-insensitive ordering

    def clean(self):
        if self.name:
            # Strip leading and trailing whitespaces from the name field if it's not None
            self.name = self.name.strip()
        super().clean()

    def __str__(self):
        # Returns the name of the topping
        return self.name

    def clean(self):
        # Check if the name is not None
        if self.name:
            # Strip leading and trailing whitespace from the topping name
            self.name = self.name.strip()
            # Check if the topping name is empty after stripping whitespace
            if not self.name:
                raise ValidationError("Topping name cannot be empty.")


# Class: Pizza
# Description: Model representing a pizza which includes toppings.
class Pizza(models.Model):
    # Name of the pizza, should be unique
    name = models.CharField(max_length=100, unique=True, blank=False, null=False, db_index=True)
    toppings = models.ManyToManyField(Topping)  # Many-to-many relationship with Topping model

    class Meta:
        ordering = [Lower('name')]  # Case-insensitive ordering

    def __str__(self):
        # Returns the name of the pizza
        return self.name

    def clean(self):
        # Check if the name is not None
        if self.name:
            # Strip leading and trailing whitespace from the pizza name
            self.name = self.name.strip()
            # Check if the pizza name is empty after stripping whitespace
            if not self.name:
                raise ValidationError("Pizza name cannot be empty.")
