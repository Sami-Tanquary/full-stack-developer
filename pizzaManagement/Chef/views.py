from django.shortcuts import render, redirect, get_object_or_404
from Owner.models import Topping, Pizza
from .forms import PizzaForm
from django.contrib.auth.decorators import login_required
from .decorators import chef_required

@chef_required
@login_required
def chef_dashboard(request):
    error_message = None
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Pizza.objects.filter(name=name).exists():
                error_message = "A pizza with this name already exists!"
            else:
                form.save()
                return redirect('chef_dashboard')
    else:
        form = PizzaForm()

    pizzas = Pizza.objects.all()

    return render(request, 'chef_dashboard.html', {'pizzas': pizzas, 'form': form, 'all_toppings': Topping.objects.all(),
                                                   'error_message': error_message})

def create_pizza(request):
    error_message = None
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            name = form.clean_name()
            if Pizza.objects.filter(name=name).exists():
                error_message = "A pizza with this name already exists!"
            else:
                form.save()
                return redirect('chef_dashboard')
        else:
            error_message = "A pizza with this name already exists!"
    else:
        form = PizzaForm()

    pizzas = Pizza.objects.all()

    return render(request, 'chef_dashboard.html', {'pizzas': pizzas, 'form': form, 'all_toppings': Topping.objects.all(),
                                                   'error_message': error_message})

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
            form.save()
            return redirect('chef_dashboard')
    else:
        form = PizzaForm(instance=pizza)

    context = {
        'pizza': pizza,
        'form': form,
        'available_toppings': available_toppings,
        'selected_toppings': selected_toppings,
    }
    return render(request, 'update_pizza.html', context)