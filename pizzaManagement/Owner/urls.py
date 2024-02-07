from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('topping/list/', views.topping_list, name='topping_list'),
    path('topping/add/', views.add_topping, name='add_topping'),
    path('topping/<int:topping_id>/delete/', views.delete_topping, name='delete_topping'),
    path('topping/<int:topping_id>/update/', views.update_topping, name='update_topping'),
]