from django.shortcuts import render
from internal.models import *


def index(request,
          template='internal/service/index.html',
          extra_context=None):
    context = {
        'service_list': Service.objects.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
