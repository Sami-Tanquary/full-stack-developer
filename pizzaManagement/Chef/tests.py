from django.test import TestCase
from Owner.models import Pizza, Topping
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PizzaForm


# -------------------------------------- CHEF DASHBOARD TESTING ---------------------------------- #
# Chef Dashboard Integration Tests
class ChefDashboardIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # Create some sample toppings
        cls.pepperoni = Topping.objects.create(name='Pepperoni')
        cls.mushrooms = Topping.objects.create(name='Mushrooms')

        # Create a sample pizza
        cls.margherita = Pizza.objects.create(name='Margherita')

        # Create an Owner user
        cls.chef_username = 'Chef'
        cls.chef_password = 'SupremeSlicesChef'
        cls.chef = User.objects.create_user(username=cls.chef_username, password=cls.chef_password)

    # Test if the Chef Dashboard view returns a 200 OK status code
    def test_chef_dashboard_view(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        response = self.client.get(reverse('chef_dashboard'))
        self.assertEqual(response.status_code, 200)

    # Test creating a new pizza through the Chef Dashboard
    def test_create_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        form_data = {'name': 'Hawaiian', 'toppings': [1, 2]}  # Assuming Pepperoni and Mushrooms have IDs 1 and 2
        response = self.client.post(reverse('chef_dashboard'), form_data)
        self.assertRedirects(response, reverse('chef_dashboard'))  # Check if redirected back to Chef Dashboard
        self.assertTrue(Pizza.objects.filter(name='Hawaiian').exists())  # Check if pizza is created in the database

    # Test creating a new pizza with invalid data
    def test_invalid_create_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        form_data = {'name': 'Margherita', 'toppings': [1]}  # Trying to create a duplicate pizza
        response = self.client.post(reverse('chef_dashboard'), form_data)
        self.assertEqual(response.status_code, 200)  # Check if form is not valid and stays on the Chef Dashboard
        self.assertFalse(Pizza.objects.filter(name='Margherita', toppings__id=1).exists())  # Check if pizza not created

    # Test creating a pizza with the maximum allowed length for the name
    def test_add_pizza_max_length_name(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        form_data = {'name': 'X' * 100, 'toppings': [1]}
        response = self.client.post(reverse('chef_dashboard'), form_data)
        self.assertRedirects(response, reverse('chef_dashboard'))
        self.assertTrue(Pizza.objects.filter(name=form_data['name']).exists())

    # Test updating an existing pizza through the Chef Dashboard
    def test_update_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        # Update sample Margherita pizza with new name and toppings
        new_name = 'Margherita Supreme'
        form_data = {'name': new_name, 'toppings': [self.pepperoni.id, self.mushrooms.id]}
        response = self.client.post(reverse('update_pizza', args=[self.margherita.id]), form_data)

        # Check if redirected back to Chef Dashboard
        self.assertRedirects(response, reverse('chef_dashboard'))

        # Get the updated pizza from the database
        updated_pizza = Pizza.objects.get(id=self.margherita.id)

        # Get the toppings for the updated pizza
        updated_toppings = list(updated_pizza.toppings.all())

        # Sort the toppings retrieved from the updated pizza
        sorted_toppings = sorted(updated_toppings, key=lambda x: x.name)

        # Check if the toppings are correctly alphabetized by database on the updated pizza
        self.assertEqual(updated_toppings, sorted_toppings)

    # Test updating a pizza with invalid data (e.g., blank name)
    def test_invalid_update_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        form_data = {'name': '', 'toppings': [self.pepperoni.id]}
        response = self.client.post(reverse('update_pizza', args=[self.margherita.id]), form_data)
        self.assertEqual(response.status_code, 200)  # Check if form is not valid and stays on the same page
        updated_pizza = Pizza.objects.get(id=self.margherita.id)
        self.assertNotEqual(updated_pizza.name, '')  # Check if pizza name is not changed

    # Test deleting an existing pizza through the Chef Dashboard
    def test_delete_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        response = self.client.post(reverse('delete_pizza', args=[self.margherita.id]))
        self.assertRedirects(response, reverse('chef_dashboard'))  # Check if redirected back to Chef Dashboard
        with self.assertRaises(Pizza.DoesNotExist):
            Pizza.objects.get(id=self.margherita.id)

    # Test deleting a pizza with invalid ID
    def test_invalid_delete_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        invalid_id = 9999
        response = self.client.post(reverse('delete_pizza', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)  # Check for not found error

    # Test attempting to update a pizza with unauthorized access
    def test_unauthorized_update_pizza(self):
        # Create a user who is not a chef
        user = User.objects.create_user(username='not_a_chef', password='test123')
        self.client.force_login(user)

        # Attempt to update a pizza
        pizza = Pizza.objects.get(name='Margherita')
        response = self.client.post(reverse('update_pizza', args=[pizza.pk]), {'name': 'New Name'})
        self.assertEqual(response.status_code, 403)  # Expect forbidden access

    # Test attempting to delete a pizza with unauthorized access
    def test_unauthorized_delete_pizza(self):
        # Create a user who is not a chef
        user = User.objects.create_user(username='not_a_chef', password='test123')
        self.client.force_login(user)

        # Get the initial count of pizzas
        initial_pizza_count = Pizza.objects.count()

        # Attempt to delete the pizza
        response = self.client.post(reverse('delete_pizza', args=[self.margherita.pk]))

        # Assert that the status code is 403 (unauthorized)
        self.assertEqual(response.status_code, 403)

        # Assert that the pizza count remains the same
        self.assertEqual(Pizza.objects.count(), initial_pizza_count)

    # Test validation to ensure at least one topping must be selected for pizza creation
    def test_empty_toppings_create_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        form_data = {'name': 'Pizza Without Toppings', 'toppings': []}  # No toppings selected
        response = self.client.post(reverse('chef_dashboard'), form_data)
        self.assertEqual(response.status_code, 200)  # Check if form is not valid and stays on the Chef Dashboard
        self.assertFalse(Pizza.objects.filter(name='Pizza Without Toppings').exists())  # Check if pizza not created

    # Test confirmation prompt for pizza deletion
    def test_confirm_delete_pizza(self):
        # Log in as the Chef user
        self.client.login(username=self.chef_username, password=self.chef_password)

        pizza = Pizza.objects.get(name='Margherita')
        response = self.client.post(reverse('delete_pizza', args=[pizza.id]), follow=True)
        self.assertContains(response, 'Are you sure you want to delete')  # Check if confirmation prompt is displayed
        self.assertContains(response, 'Delete')  # Check if the delete button is present


# ------------------------------------- PIZZA FORM TESTING ------------------------------------ #
class PizzaFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test toppings
        cls.pepperoni = Topping.objects.create(name='Pepperoni')
        cls.mushrooms = Topping.objects.create(name='Mushrooms')

    def test_valid_form(self):
        # Create a valid form data
        form_data = {'name': 'Pepperoni Pizza', 'toppings': [self.pepperoni.id, self.mushrooms.id]}
        form = PizzaForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test for blank name field
    def test_blank_name(self):
        form_data = {'name': '', 'toppings': [self.pepperoni.id]}  # Assuming there is at least one topping available
        form = PizzaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

    # Test for name exceeding maximum length
    def test_max_length_name(self):
        form_data = {'name': 'X' * 101, 'toppings': [self.pepperoni.id]}  # Exceeding maximum length of 100
        form = PizzaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

    # Test for a duplicate name
    def test_duplicate_name(self):
        Pizza.objects.create(name='Margherita')
        form_data = {'name': 'Margherita', 'toppings': [self.pepperoni.id]}  # Trying to create a duplicate pizza
        form = PizzaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

    # Test for name with leading and trailing whitespaces
    def test_name_with_whitespace(self):
        # Create form data with leading and trailing whitespaces in the name field
        form_data = {'name': '  Margherita  ', 'toppings': [self.pepperoni.id]}
        # Create the form instance
        form = PizzaForm(data=form_data)
        # Check if the form is valid after cleaning
        self.assertTrue(form.is_valid())
        # Check if the cleaned name field has leading and trailing whitespaces stripped
        self.assertEqual(form.cleaned_data['name'], 'Margherita')

    # Test for updating existing topping to ensure model doesn't think it's a new unique pizza
    def test_unique_name_validation(self):
        # Create a pizza with a unique name
        pizza = Pizza.objects.create(name='Unique Pizza')

        # Attempt to update a pizza keeping the name the same
        form_data = {'name': 'Unique Pizza', 'toppings': [self.pepperoni.id]}
        form = PizzaForm(data=form_data, instance=pizza)

        # Verify that the form is valid because this is not a duplicate pizza
        self.assertTrue(form.is_valid())


# ------------------------------------- AUTHENTICATION TESTING ------------------------------- #
# Tests for Chef Login
class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test Chef user
        cls.owner_username = 'Chef'
        cls.owner_password = 'SupremeSlicesChef'
        cls.owner = User.objects.create_user(username=cls.owner_username, password=cls.owner_password)

    def test_valid_owner_login(self):
        # Attempt to log in as Chef with correct credentials
        response = self.client.post(reverse('home'), {'username': self.owner_username, 'password': self.owner_password}, follow=True)
        # Check if user is authenticated and redirected to Owner dashboard
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('chef_dashboard'))

    def test_invalid_owner_login(self):
        # Attempt to log in as Chef with incorrect credentials
        response = self.client.post(reverse('home'), {'username': self.owner_username, 'password': 'wrong_password'}, follow=True)
        # Check if user is not authenticated and error message is displayed
        self.assertFalse(response.context['user'].is_authenticated)
