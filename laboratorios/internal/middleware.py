from django.shortcuts import (
    HttpResponseRedirect,
    redirect
)
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.urlresolvers import reverse_lazy


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated() and request.path != '/internal/login':
            return redirect('internal:login')
        return None
