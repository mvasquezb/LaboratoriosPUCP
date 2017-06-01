from django.shortcuts import (
    render,
    get_object_or_404
)
from django.http import JsonResponse
from django.template.loader import render_to_string

from internal.models import *
from . import forms


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
    parameter_forms = forms.ParameterFillFormset(
        queryset=test.parameterfill_set.all()
    )

    context = {
        'service': service,
        'essay': essay,
        'test': test,
        'parameter_forms': parameter_forms,
    }
    if extra_context is not None:
        context.update(extra_context)
    if request.is_ajax() or request.GET.get('type') == 'json':
        template = 'internal/testfill/show.table.html'
        rendered = render_to_string(template, context, request)
        return JsonResponse({
            'success': True,
            'render': rendered,
        }, json_dumps_params={'ensure_ascii': False})
    return render(request, template, context)


def update(request,
           service_id,
           essay_id,
           test_id):
    print(request.POST)
    parameter_forms = forms.ParameterFillFormset(request.POST)
    if parameter_forms.is_valid():
        parameters = parameter_forms.save()
        print(parameters)
    return render(request, 'internal/testfill/show.html', {})
