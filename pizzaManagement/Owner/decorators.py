from django.http import HttpResponseForbidden


# Function: owner_required
# Parameters:
#   - view_func: The view function to be wrapped
# Description: Decorator function that checks if the user is authenticated and is an owner.
#              If the user is authenticated and is an owner, the wrapped view function is called.
#              Otherwise, returns an HTTP 403 Forbidden response.
# Returns: The wrapped view function.
def owner_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and is an owner
        if request.user.is_authenticated and request.user.username == 'Owner':
            # Call the view function
            return view_func(request, *args, **kwargs)
        else:
            # Return HTTP 403 Forbidden response if not authenticated or not an owner
            return HttpResponseForbidden("You don't have permission to access this page.")
    return wrapped_view
