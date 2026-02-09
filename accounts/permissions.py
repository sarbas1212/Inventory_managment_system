from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role in allowed_roles or request.user.role == 'ADMIN':
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

def admin_only(view_func):
    return role_required(['ADMIN'])(view_func)

def accountant_needed(view_func):
    return role_required(['ADMIN', 'ACCOUNTANT'])(view_func)
