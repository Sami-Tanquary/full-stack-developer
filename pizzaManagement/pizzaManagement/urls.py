from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import CustomLoginView, CustomLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('owner/', include('Owner.urls')),
    path('chef/', include('Chef.urls')),
    path('', CustomLoginView.as_view(), name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

