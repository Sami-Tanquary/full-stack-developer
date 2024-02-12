from django.db import models


# Class: Topping
# Description: Model representing a pizza topping.
class Topping(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the topping, should be unique

    def __str__(self):
        # Returns the name of the topping
        return self.name


# Class: Pizza
# Description: Model representing a pizza which includes toppings.
class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the pizza, should be unique
    toppings = models.ManyToManyField(Topping)  # Many-to-many relationship with Topping model

    def __str__(self):
        # Returns the name of the pizza
        return self.name
