from django.shortcuts import render, redirect, get_object_or_404
from .models import Topping
from .forms import ToppingForm
from django.contrib.auth.decorators import login_required
from .decorators import owner_required

# Function: owner_dashboard
# Parameters: request (HttpRequest)
# Description: Displays the owner dashboard with the list of toppings and a form to add new toppings.
#              Requires Owner authentication to access
# Returns: HttpResponse
@owner_required
@login_required
def owner_dashboard(request):
    # Set error message to None by default
    error_message = None
    # Check if HTTP request method is POST
    if request.method == 'POST':
        # Create Topping form based on request
        form = ToppingForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Check if topping name is duplicate
            name = form.cleaned_data['name']
            # If duplicate, set error message
            if Topping.objects.filter(name=name).exists():
                error_message = "This topping already exists!"
            # Else, save form and redirect back to owner dashboard
            else:
                form.save()
                return redirect('owner_dashboard')
        else:
            # If form is invalid, set error message
            error_message = "This topping already exists!"
    else:
        # If not a POST request, initialize an empty form
        form = ToppingForm()

    # Order toppings alphabetically by name
    toppings = Topping.objects.order_by('name')

    # Render the owner_dashboard.html template with toppings, form, and error message
    return render(request, 'owner_dashboard.html', {'toppings': toppings, 'form': form,
                                                    'error_message': error_message})


# Function: topping_list
# Parameters: request (HttpRequest)
# Description: Renders a list of toppings ordered alphabetically by name.
# Returns: HttpResponse
def topping_list(request):
    # Order toppings alphabetically by name
    toppings = Topping.objects.order_by('name')
    # Render the owner_dashboard.html template with available toppings
    return render(request, 'owner_dashboard.html', {'toppings': toppings})


# Function: add_topping
# Parameters: request (HttpRequest)
# Description: Handles the addition of a new topping.
#              If the form data is valid and the topping does not already exist,
#              it saves the topping and redirects to the topping list page,
#              otherwise, it displays an error message.
# Returns: HttpResponse
def add_topping(request):
    # Initialize error_message as None
    error_message = None
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = ToppingForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Extract the name of the topping from the form data
            name = form.cleaned_data['name']
            # Check if a topping with the same name already exists
            if Topping.objects.filter(name=name).exists():
                # Set error_message if the topping already exists
                error_message = "This topping already exists!"
            else:
                # Save the new topping and redirect to the topping list page
                form.save()
                return redirect('topping_list')
        else:
            # Set error_message if the form is invalid
            error_message = "This topping already exists!"
    # If the request method is not POST, initialize an empty form
    else:
        form = ToppingForm()

    # Order toppings alphabetically by name
    toppings = Topping.objects.order_by('name')

    # Render the owner dashboard with the form, toppings, and error_message
    return render(request, 'owner_dashboard.html', {'form': form, 'toppings': toppings, 'error_message': error_message})


# Function: delete_topping
# Parameters: request (HttpRequest), topping_id (int)
# Description: Deletes a topping with the given topping_id.
#              If the request method is POST, it deletes the topping and
#              redirects to the topping list page. Otherwise, it renders
#              the owner dashboard with information about the topping.
# Returns: HttpResponse
def delete_topping(request, topping_id):
    # Retrieve the topping object with the given topping_id or return a 404 error
    topping = get_object_or_404(Topping, pk=topping_id)
    # Check if the request method is POST
    if request.method == 'POST':
        # If POST, delete the topping and redirect to the topping list page
        topping.delete()
        return redirect('topping_list')
    # If not a POST request, render the owner dashboard with information about the topping
    return render(request, 'owner_dashboard.html', {'topping': topping})


# Function: update_topping
# Parameters: request (HttpRequest), topping_id (int)
# Description: Updates the topping with the given topping_id.
#              If the request method is POST, it updates the
#              topping with the form data and redirects to the
#              topping list page. Otherwise, it renders the owner
#              dashboard with the topping update form.
# Returns: HttpResponse
def update_topping(request, topping_id):
    # Retrieve the topping object with the given topping_id or return a 404 error
    topping = get_object_or_404(Topping, pk=topping_id)
    # Check if the request method is POST
    if request.method == 'POST':
        # If POST, create a form instance with the POST data and the instance of the topping
        form = ToppingForm(request.POST, instance=topping)
        # Check if the form is valid
        if form.is_valid():
            # If valid, save the form and redirect to the topping list page
            form.save()
            return redirect('topping_list')
    else:
        # If not a POST request, create a form instance with the instance of the topping
        form = ToppingForm(instance=topping)
    # Render the owner dashboard with the topping update form
    return render(request, 'owner_dashboard.html', {'form': form, 'topping': topping})