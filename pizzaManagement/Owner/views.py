from django.shortcuts import render, redirect, get_object_or_404
from .models import Topping
from .forms import ToppingForm
from django.contrib.auth.decorators import login_required
from .decorators import owner_required


@owner_required
@login_required
def owner_dashboard(request):
    if request.method == 'POST':
        form = ToppingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Topping.objects.filter(name=name).exists():
                # Topping with the same name already exists
                context = {'form': form, 'toppings': Topping.objects.all(), 'error_message': 'Topping already exists!'}
                return render(request, 'owner_dashboard.html', context)
            else:
                form.save()
                return redirect('owner_dashboard')
    else:
        form = ToppingForm()

    toppings = Topping.objects.all()

    return render(request, 'owner_dashboard.html', {'toppings': toppings, 'form': form})


def topping_list(request):
    toppings = Topping.objects.all()
    return render(request, 'owner_dashboard.html', {'toppings': toppings})


def add_topping(request):
    if request.method == 'POST':
        form = ToppingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topping_list')
    else:
        form = ToppingForm()
    return render(request, 'owner_dashboard.html', {'form': form})


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
