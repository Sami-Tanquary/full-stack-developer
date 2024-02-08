from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.chef_dashboard, name='chef_dashboard'),
    path('create/', views.create_pizza, name='create_pizza'),
    path('delete/<int:pizza_id>/', views.delete_pizza, name='delete_pizza'),
    path('update_pizza/<int:pizza_id>/', views.update_pizza, name='update_pizza'),
]
