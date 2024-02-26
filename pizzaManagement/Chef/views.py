from django.shortcuts import render, redirect, get_object_or_404
from Owner.models import Topping, Pizza, Crust
from .forms import PizzaForm
from django.contrib.auth.decorators import login_required
from .decorators import chef_required


# Function: chef_dashboard
# Parameters: request (HttpRequest)
# Description: Renders the chef dashboard page with a form to create new pizzas, a list of existing pizzas,
#              and a list of all toppings ordered alphabetically by name. Handles form submission to create new pizzas.
#              Requires Chef authentication to access.
# Returns: HttpResponse
@chef_required
@login_required
def chef_dashboard(request):
    # Initialize error_message as None
    error_message = None
    # Check if request method is POST
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = PizzaForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Extract the name of the pizza from the form data
            name = form.cleaned_data['name']
            # If duplicate, set error message
            if Pizza.objects.filter(name__iexact=name).exists():
                error_message = "A pizza with this name already exists!"
            # Else, save form and redirect to chef dashboard
            else:
                form.save()
                return redirect('chef_dashboard')
    # If not a POST request, initialize an empty form
    else:
        form = PizzaForm()

    # Grab all currently populated pizzas from model
    pizzas = Pizza.objects.all()
    # Order toppings by name alphabetically
    toppings = Topping.objects.order_by('name')
    # Order crusts by name alphabetically
    crusts = Crust.objects.order_by('name')

    # Render the request to chef_dashboard with all context {pizzas, form, toppings, any errors}
    return render(request, 'chef_dashboard.html', {'pizzas': pizzas, 'form': form, 'all_toppings': toppings,
                                                   'all_crusts': crusts,
                                                   'error_message': error_message})


# Function: create_pizza
# Parameters: request (HttpRequest)
# Description: Handles the creation of a new pizza. Validates form input, checks for duplicate pizza names,
#              and saves the new pizza if it does not already exist.
# Returns: HttpResponse
@chef_required
def create_pizza(request):
    # Initialize error message to None
    error_message = None
    # Check if HTTP request method is POST
    if request.method == 'POST':
        # Create PizzaForm instance with POST data
        form = PizzaForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get cleaned name from form
            name = form.clean_name()
            # Check if pizza name already exists
            if Pizza.objects.filter(name__iexact=name).exists():
                # Set error message if pizza name already exists
                error_message = "A pizza with this name already exists!"
            else:
                # Save form data and redirect to chef dashboard
                form.save()
                return redirect('chef_dashboard')
        else:
            # Set error message if form is invalid
            error_message = "A pizza with this name already exists!"
    else:
        # If not a POST request, initialize an empty form
        form = PizzaForm()

    # Retrieve all pizzas and toppings ordered alphabetically
    pizzas = Pizza.objects.all()
    toppings = Topping.objects.order_by('name')

    # Render chef dashboard with form, pizzas, toppings, and error message
    return render(request, 'chef_dashboard.html', {'pizzas': pizzas, 'form': form, 'all_toppings': toppings,
                                                   'error_message': error_message})


# Function: delete_pizza
# Parameters: request (HttpRequest), pizza_id (int)
# Description: Deletes a pizza with the given pizza_id.
# Returns: HttpResponse
@chef_required
def delete_pizza(request, pizza_id):
    # Get the pizza object with the given pizza_id or return a 404 error if not found
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    # Delete the pizza object
    pizza.delete()
    # Redirect to the chef dashboard
    return redirect('chef_dashboard')


# Function: update_pizza
# Parameters: request (HttpRequest), pizza_id (int)
# Description: Allows the Chef to update an existing pizza with the given pizza_id.
# Returns: HttpResponse
@chef_required
def update_pizza(request, pizza_id):
    # Get the pizza object with the given pizza_id or return a 404 error if not found
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    # Get all toppings ordered by name alphabetically
    available_toppings = Topping.objects.order_by('name')
    # Get the toppings selected for the pizza
    selected_toppings = pizza.toppings.all()
    #Get the selected crust for the pizza
    selected_crust = pizza.crust
    # Get all crusts ordered by name alphabetically
    all_crusts = Crust.objects.order_by('name')

    # Check if HTTP request method is POST
    if request.method == 'POST':
        # Create a PizzaForm instance with POST data and the pizza instance
        form = PizzaForm(request.POST, instance=pizza)
        # Check if form is valid
        if form.is_valid():
            # Save the form and redirect to the chef dashboard
            form.save()
            return redirect('chef_dashboard')
    else:
        # If not a POST request, create a form with the pizza instance
        form = PizzaForm(instance=pizza)

    # Prepare context with pizza object, form, available toppings, and selected toppings
    context = {
        'pizza': pizza,
        'form': form,
        'available_toppings': available_toppings,
        'selected_toppings': selected_toppings,
        'selected_crust': selected_crust,
        'all_crusts': all_crusts,
    }
    # Render the update_pizza.html template with the context
    return render(request, 'update_pizza.html', context)
