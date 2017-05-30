from django.shortcuts import (
    render,
    get_object_or_404
)
from internal.models import *


def index(request,
          service_id,
          essay_id,
          template='internal/testfill/index.html',
          extra_context=None):
    service = get_object_or_404(Service, pk=service_id)
    essay = get_object_or_404(service.essays, pk=essay_id)
    test_list = essay.testfill_set.all()

    context = {
        'service': service,
        'essay': essay,
        'test_list': test_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         service_id,
         essay_id,
         test_id,
         template='internal/testfill/show.html',
         extra_context=None):
    service = get_object_or_404(Service, pk=service_id)
    essay = get_object_or_404(service.essays, pk=essay_id)
    test = get_object_or_404(essay.testfill_set, pk=test_id)

    context = {
        'service': service,
        'essay': essay,
        'test': test,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
