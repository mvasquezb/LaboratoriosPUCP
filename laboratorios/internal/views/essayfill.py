from django.shortcuts import (
    render,
    get_object_or_404
)
from internal.models import *


def index(request,
          service_id,
          template='internal/essayfill/index.html',
          extra_context=None):
    service = get_object_or_404(Service, pk=service_id)
    essay_list = service.essays.all()
    context = {
        'service': service,
        'essay_list': essay_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         service_id,
         essay_id,
         template='internal/essayfill/show.html',
         extra_context=None):
    service = get_object_or_404(Service, pk=service_id)
    essay = get_object_or_404(service.essays, pk=essay_id)
    context = {
        'service': service,
        'essay': essay,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
