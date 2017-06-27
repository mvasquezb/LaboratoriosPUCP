from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.conf import settings

from urllib.parse import urlparse
from functools import wraps, partial
from django.contrib import messages


def permission_check(user, permissions):
    if user.is_superuser:
        return True
    if not hasattr(user, 'basicuser'):
        return False
    if not isinstance(permissions, (list, tuple)):
        permissions = [permissions]
    permission_list = user.basicuser.permissions
    return permission_list.filter(
        codename__in=permissions
    ).exists()


def set_permission_check(permissions):
    return partial(permission_check, permissions=permissions)


fail_permission_message = 'Necesita permisos para ejecutar esa acción'


def user_passes_test(test_func,
                     login_url=None,
                     redirect_field_name=REDIRECT_FIELD_NAME,
                     message=fail_permission_message):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            # Added this message line
            messages.error(request, message)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator
