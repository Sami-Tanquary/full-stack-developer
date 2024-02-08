from django.shortcuts import render, redirect, get_object_or_404
from Owner.models import Topping, Pizza
from .forms import PizzaForm
from django.contrib.auth.decorators import login_required
from .decorators import chef_required


@chef_required
@login_required
def chef_dashboard(request):
    pizzas = Pizza.objects.all()
    return render(request, 'chef_dashboard.html', {'pizzas': pizzas})


def create_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chef_dashboard')
    else:
        form = PizzaForm()
    return render(request, 'chef_dashboard.html', {'form': form})


def delete_pizza(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    pizza.delete()
    return redirect('chef_dashboard')


def update_pizza(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    available_toppings = Topping.objects.all()
    selected_toppings = pizza.toppings.all()

    if request.method == 'POST':
        form = PizzaForm(request.POST, instance=pizza)
        if form.is_valid():
            # Save the form to update the pizza instance with the new toppings
            form.save()
            return redirect('chef_dashboard')
    else:
        # Pass the form to the template
        form = PizzaForm(instance=pizza)

    context = {
        'pizza': pizza,
        'form': form,
        'available_toppings': available_toppings,
        'selected_toppings': selected_toppings,
    }
    return render(request, 'update_pizza.html', context)