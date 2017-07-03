from .main import *
from .client import *
from .employee import *
from .laboratory import *
from .essaymethod import *
from .role import *
from .servicerequest import *
from .inventoryOrder import *
from .servicecontract import *
from .sampleType import *
from .essay import *
from .inventoryItem import *
from .parameterfill import *
from .reports import *
from .supply import *
from .equipment import *
from .externalprovider import *
from .inventory import *


import django.contrib.auth.views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from internal.models import Client
from django.contrib import messages


def login(request, extra_context=None):
    params = {
        'template_name': 'internal/login.html',
        'redirect_authenticated_user': True,
    }
    auth_message = request.session.pop('auth_message', '')
    extra_context = extra_context or {}
    extra_context['auth_message'] = auth_message
    params['extra_context'] = extra_context
    is_post = request.method == 'POST'
    if is_post:
        username = request.POST.get('username', '')
        try:
            client = Client.all_objects.get(
                deleted__isnull=True,
                user__username=username
            )
            messages.error(
                request,
                'El módulo del cliente está en construcción.'
                ' Por favor intente con un usuario diferente'
            )
            return redirect('internal:login')
        except Client.DoesNotExist:
            pass

    response = auth_views.login(request, **params)
    return response
