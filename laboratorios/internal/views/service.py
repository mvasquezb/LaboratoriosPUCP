from django.shortcuts import (
    render,
    get_object_or_404
)
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


def show(request,
         pk,
         template='internal/service/show.html',
         extra_context=None):
    service = get_object_or_404(Service, pk=pk)
    context = {
        'service': service,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
