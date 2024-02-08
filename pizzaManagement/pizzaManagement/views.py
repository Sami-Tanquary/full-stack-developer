from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = 'home.html'  # This is where the login form will be displayed

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.username == 'Chef':
                return reverse('chef_dashboard')  # Redirect to Chef dashboard
            elif user.username == 'Owner':
                return reverse('owner_dashboard')  # Redirect to Owner dashboard
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Redirect to the home page after logout

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Redirect to the home page after logout
        return redirect(self.next_page)
