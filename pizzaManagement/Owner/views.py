from django.shortcuts import render, redirect, get_object_or_404
from .models import Topping
from .forms import ToppingForm
from django.contrib.auth.decorators import login_required
from .decorators import owner_required


@owner_required
@login_required
def owner_dashboard(request):
    error_message = None
    if request.method == 'POST':
        form = ToppingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Topping.objects.filter(name=name).exists():
                error_message = "This topping already exists!"
            else:
                form.save()
                return redirect('owner_dashboard')
        else:
            error_message = "This topping already exists!"
    else:
        form = ToppingForm()

    toppings = Topping.objects.all()

    return render(request, 'owner_dashboard.html', {'toppings': toppings, 'form': form,
                                                    'error_message': error_message})


def topping_list(request):
    toppings = Topping.objects.all()
    return render(request, 'owner_dashboard.html', {'toppings': toppings})


def add_topping(request):
    error_message = None
    if request.method == 'POST':
        form = ToppingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Topping.objects.filter(name=name).exists():
                error_message = "This topping already exists!"
            else:
                form.save()
                return redirect('topping_list')
        else:
            error_message = "This topping already exists!"
    else:
        form = ToppingForm()

    toppings = Topping.objects.all()

    return render(request, 'owner_dashboard.html', {'form': form, 'toppings': toppings, 'error_message': error_message})


def delete_topping(request, topping_id):
    topping = get_object_or_404(Topping, pk=topping_id)
    if request.method == 'POST':
        topping.delete()
        return redirect('topping_list')
    return render(request, 'owner_dashboard.html', {'topping': topping})


def update_topping(request, topping_id):
    topping = get_object_or_404(Topping, pk=topping_id)
    if request.method == 'POST':
        form = ToppingForm(request.POST, instance=topping)
        if form.is_valid():
            form.save()
            return redirect('topping_list')
    else:
        form = ToppingForm(instance=topping)
    return render(request, 'owner_dashboard.html', {'form': form, 'topping': topping})
