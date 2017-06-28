import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils.deprecation import MiddlewareMixin

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class AuthRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.

    Based on https://djangosnippets.org/snippets/1179/
    My modification adds 'next' GET parameter to enable redirection after
    successful login.
    """

    def process_request(self, request):
        if not hasattr(request, 'user'):
            return
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                # Add 'next' GET variable to support redirection after login
                if len(path) > 0 and is_safe_url(
                    url=request.path_info,
                    host=request.get_host()
                ):
                    redirect_to = "{}?next={}".format(
                        settings.LOGIN_URL,
                        request.path_info
                    )
                return HttpResponseRedirect(redirect_to)
