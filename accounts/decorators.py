from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for views that checks if the user has the required role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # If role not allowed
            messages.error(request, "You do not have permission to access this page.")
            if request.user.role == 'Customer':
                return redirect('customer_dashboard')
            elif request.user.role == 'Vendor':
                return redirect('vendor_dashboard')
            else:
                return redirect('home')
                
        return _wrapped_view
    return decorator
