from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated() and request.path != '/internal/login':
            return redirect('internal:login')
        return None
