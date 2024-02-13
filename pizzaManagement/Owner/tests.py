from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from .models import Pizza, Topping
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ToppingForm


# ----------------------------- OWNER DASHBOARD TESTING --------------------------- #
class OwnerDashboardIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # Create some sample toppings
        Topping.objects.create(name='Pepperoni')
        Topping.objects.create(name='Mushrooms')

        # Create an Owner user
        cls.owner_username = 'Owner'
        cls.owner_password = 'SupremeSlicesOwner'
        cls.owner = User.objects.create_user(username=cls.owner_username, password=cls.owner_password)

    # Test if the Owner Dashboard view returns a 200 OK status code
    def test_owner_dashboard_view(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        response = self.client.get(reverse('owner_dashboard'))
        self.assertEqual(response.status_code, 200)

    # Test adding a new topping through the Owner Dashboard
    def test_add_topping(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        form_data = {'name': 'Olives'}  # Adding a new topping named Olives
        response = self.client.post(reverse('owner_dashboard'), form_data)
        self.assertRedirects(response, reverse('owner_dashboard'))  # Check if redirected back to Owner Dashboard
        self.assertTrue(Topping.objects.filter(name='Olives').exists())  # Check if topping is created in the database

    # Test adding a new topping with invalid data (duplicate)
    def test_invalid_add_topping(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        # Count the number of toppings named "Pepperoni" before the form submission
        initial_pepperoni_count = Topping.objects.filter(name='Pepperoni').count()

        # Attempt to create a duplicate topping named "Pepperoni"
        form_data = {'name': 'Pepperoni'}
        response = self.client.post(reverse('owner_dashboard'), form_data)

        # Check if form is not valid and stays on the Owner Dashboard
        self.assertEqual(response.status_code, 200)

        # Count the number of toppings named "Pepperoni" after the form submission
        updated_pepperoni_count = Topping.objects.filter(name='Pepperoni').count()

        # Assert that the number of toppings named "Pepperoni" remains the same
        self.assertEqual(initial_pepperoni_count, updated_pepperoni_count)

    # Test adding a topping with the maximum allowed length for the name
    def test_add_topping_max_length_name(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        form_data = {'name': 'X' * 100}  # Maximum allowed length for the name
        response = self.client.post(reverse('owner_dashboard'), form_data)
        self.assertRedirects(response, reverse('owner_dashboard'))
        self.assertTrue(Topping.objects.filter(name=form_data['name']).exists())

    # Test updating an existing topping through the Owner Dashboard
    def test_update_topping(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        topping = Topping.objects.get(name='Pepperoni')
        new_name = 'Spicy Pepperoni'
        form_data = {'name': new_name}
        response = self.client.post(reverse('update_topping', args=[topping.id]), form_data)
        # Check if redirected back to Owner Dashboard
        self.assertRedirects(response, reverse('topping_list'))
        updated_topping = Topping.objects.get(id=topping.id)
        self.assertEqual(updated_topping.name, new_name)

    # Test deleting an existing topping through the Owner Dashboard
    def test_delete_topping(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        topping = Topping.objects.get(name='Pepperoni')
        response = self.client.post(reverse('delete_topping', args=[topping.id]))
        self.assertRedirects(response, reverse('topping_list'))  # Check if redirected back to topping list
        with self.assertRaises(Topping.DoesNotExist):
            Topping.objects.get(id=topping.id)

    # Test appropriate error messages are displayed for invalid data
    def test_error_messages(self):
        # Log in as the Owner user
        self.client.login(username=self.owner_username, password=self.owner_password)

        # Test adding a topping with blank name
        form_data = {'name': ''}
        response = self.client.post(reverse('owner_dashboard'), form_data)
        self.assertFormError(response, 'form', 'name', 'This field is required.')


# --------------------------------- MODEL TESTING ------------------------------- #
# Tests for Pizza model
class PizzaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Pizza.objects.create(name='Pepperoni')

    # Test that name field is correctly labeled
    def test_name_label(self):
        pizza = Pizza.objects.get(id=1)
        field_label = pizza._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    # Test correct max length constraint for name
    def test_name_max_length(self):
        pizza = Pizza.objects.get(id=1)
        max_length = pizza._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_name(self):
        pizza = Pizza.objects.get(id=1)
        expected_object_name = pizza.name
        self.assertEquals(expected_object_name, str(pizza))

    # Attempt to create another pizza with the same name
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Pizza.objects.create(name='Pepperoni')

    # Attempt to create a pizza with a blank name
    def test_blank_name(self):
        pizza = Pizza(name='')
        with self.assertRaises(ValidationError):
            pizza.full_clean()

    # Attempt to create a pizza with a null name
    def test_null_name(self):
        pizza = Pizza(name=None)
        with self.assertRaises(ValidationError):
            pizza.full_clean()

    # Test for pizza name with leading and trailing whitespaces
    def test_name_with_whitespace(self):
        # Create a pizza with leading and trailing whitespaces
        pizza = Pizza(name='  Margherita  ')
        # Clean the pizza (this should strip whitespaces)
        pizza.full_clean()
        # Verify that the name is stripped
        self.assertEqual(pizza.name, 'Margherita')

    # Ensure that the unique constraint on name is case-insensitive
    def test_name_with_unique_constraint_case_insensitive(self):
        # Create a pizza with a name in lowercase
        Pizza.objects.create(name='pepperoni')
        # Attempt to create another pizza with the same name but different case
        with self.assertRaises(IntegrityError):
            Pizza.objects.create(name='Pepperoni')

    # Test creating a pizza with valid data
    def test_valid_pizza_creation(self):
        pizza = Pizza.objects.create(name='Margarita')
        self.assertTrue(Pizza.objects.filter(name='Margarita').exists())

    # Test creating pizzas with different valid name formats
    def test_valid_name_formats(self):
        valid_names = ['Margherita', 'Veggie Supreme', 'Hawaiian', '4 Cheese']
        for name in valid_names:
            pizza = Pizza.objects.create(name=name)
            self.assertTrue(Pizza.objects.filter(name=name).exists())

    # Test creating a pizza with Unicode characters in the name
    def test_unicode_characters(self):
        pizza_name = '🍕 Margherita 🍕'
        pizza = Pizza.objects.create(name=pizza_name)
        self.assertTrue(Pizza.objects.filter(name=pizza_name).exists())

    # Test creating a pizza with a name at the boundary of the maximum length
    def test_name_length_boundary(self):
        max_length_name = 'X' * 100
        pizza = Pizza.objects.create(name=max_length_name)
        self.assertTrue(Pizza.objects.filter(name=max_length_name).exists())


# Test for Topping model
class ToppingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Topping.objects.create(name='Cheese')

    # Test that name field is correctly labeled
    def test_name_label(self):
        topping = Topping.objects.get(id=1)
        field_label = topping._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    # Test correct max length constraint for name
    def test_name_max_length(self):
        topping = Topping.objects.get(id=1)
        max_length = topping._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_name(self):
        topping = Topping.objects.get(id=1)
        expected_object_name = topping.name
        self.assertEquals(expected_object_name, str(topping))

    # Attempt to create another topping with the same name
    def test_unique_name(self):
        with self.assertRaises(Exception) as context:
            Topping.objects.create(name='Cheese')

    # Test creating a topping with valid data
    def test_valid_topping_creation(self):
        topping = Topping.objects.create(name='Mushrooms')
        self.assertTrue(Topping.objects.filter(name='Mushrooms').exists())

    # Test creating toppings with different valid name formats
    def test_valid_name_formats(self):
        valid_names = ['Olives', 'Pepperoni', 'Onions', 'Bell Peppers']
        for name in valid_names:
            topping = Topping.objects.create(name=name)
            self.assertTrue(Topping.objects.filter(name=name).exists())

    # Test creating a topping with Unicode characters in the name
    def test_unicode_characters(self):
        topping_name = '🍄 Mushrooms 🍄'
        topping = Topping.objects.create(name=topping_name)
        self.assertTrue(Topping.objects.filter(name=topping_name).exists())

    # Test creating a topping with a name at the boundary of the maximum length
    def test_name_length_boundary(self):
        max_length_name = 'X' * 100
        topping = Topping.objects.create(name=max_length_name)
        self.assertTrue(Topping.objects.filter(name=max_length_name).exists())


# ----------------------------- TOPPING FORM TESTING ----------------------------- #
class ToppingFormTest(TestCase):
    def test_valid_form(self):
        # Create a valid form data
        form_data = {'name': 'Cheese'}
        form = ToppingForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test for blank name field
    def test_blank_name(self):
        form_data = {'name': ''}
        form = ToppingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

    # Test for name exceeding maximum length
    def test_max_length_name(self):
        form_data = {'name': 'X' * 101}  # Exceeding maximum length of 100
        form = ToppingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

    # Test for a duplicate name
    def test_duplicate_name(self):
        Topping.objects.create(name='Olives')
        form_data = {'name': 'Olives'}  # Trying to create a duplicate topping
        form = ToppingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

    # Test for updating existing topping to ensure model doesn't think it's a new unique topping
    def test_unique_name_validation(self):
        # Create a topping with a unique name
        topping = Topping.objects.create(name='Unique Topping')

        # Attempt to update with the same name
        form_data = {'name': 'Unique Topping'}
        form = ToppingForm(data=form_data, instance=topping)

        # Verify that the form is valid because this is not a duplicate topping
        self.assertTrue(form.is_valid())


# ---------------------------- AUTHENTICATION TESTING ---------------------------- #
# Tests for Owner Login
class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test Owner user
        cls.owner_username = 'Owner'
        cls.owner_password = 'SupremeSlicesOwner'
        cls.owner = User.objects.create_user(username=cls.owner_username, password=cls.owner_password)

    def test_valid_owner_login(self):
        # Attempt to log in as Owner with correct credentials
        response = self.client.post(reverse('home'), {'username': self.owner_username, 'password': self.owner_password}, follow=True)
        # Check if user is authenticated and redirected to Owner dashboard
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('owner_dashboard'))

    def test_invalid_owner_login(self):
        # Attempt to log in as Owner with incorrect credentials
        response = self.client.post(reverse('home'), {'username': self.owner_username, 'password': 'wrong_password'}, follow=True)
        # Check if user is not authenticated and error message is displayed
        self.assertFalse(response.context['user'].is_authenticated)