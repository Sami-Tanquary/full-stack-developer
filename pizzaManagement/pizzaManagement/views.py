from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect


# Function: CustomLoginView
# Parameters: LoginView
# Description: Customizes the login view.
#              Sets the template name where the login form
#              will be displayed and defines the logic for
#              redirecting users to their respective dashboards
#              after successful login.
# Returns: Success URL for redirecting users after successful login
class CustomLoginView(LoginView):
    template_name = 'home.html'  # This is where the login form will be displayed

    def get_success_url(self):
        # Retrieve the authenticated user
        user = self.request.user
        # Check if the user is authenticated
        if user.is_authenticated:
            # If user is a Chef, redirect to Chef dashboard
            if user.username == 'Chef':
                return reverse('chef_dashboard')
            # If user is an Owner, redirect to Owner dashboard
            elif user.username == 'Owner':
                return reverse('owner_dashboard')
        # If user is not authenticated or not Chef/Owner, redirect to default success URL
        return super().get_success_url()


# Function: CustomLogoutView
# Parameters: LogoutView
# Description: Customizes the logout view. Sets the next page to redirect to after logout to the home page.
# Returns: Redirects to the home page after logout
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Redirect to the home page after logout

    def dispatch(self, request, *args, **kwargs):
        # Call the dispatch method of the parent class
        response = super().dispatch(request, *args, **kwargs)
        # Redirect to the home page after logout
        return redirect(self.next_page)