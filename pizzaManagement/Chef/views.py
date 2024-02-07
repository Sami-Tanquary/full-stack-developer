from django.shortcuts import render
from Owner.models import Pizza


def chef_dashboard(request):
    pizzas = Pizza.objects.all()
    return render(request, 'chef_dashboard.html', {'pizzas': pizzas})
