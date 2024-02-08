from django.http import HttpResponseForbidden


def chef_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.username == 'Chef':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")
    return wrapped_view
