from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.chef_dashboard, name='chef_dashboard'),
    # Add other URLs for chef functionalities
]