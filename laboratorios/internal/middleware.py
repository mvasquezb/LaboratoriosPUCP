from django.shortcuts import redirect
from django.conf import settings
from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'user'):
            return
        if not request.user.is_authenticated() and request.path != settings.LOGIN_URL:
            GET = QueryDict(mutable=True)
            GET.update({'next': request.path})
            redirect_to = '{}?{}'.format(settings.LOGIN_URL, GET.urlencode())
            return redirect(redirect_to)
        return None
