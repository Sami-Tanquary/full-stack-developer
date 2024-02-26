from django.contrib import admin

# Register your models here.

from .models import Pizza, Topping, Crust

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Crust)
