from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum

from internal.models import *


def show(request,
         request_id):
    return HttpResponse('Show')


def quotation(request,
              request_id,
              template='internal/servicerequest/quotation.html',
              extra_context=None):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)
    quotation, created = Quotation.objects.get_or_create(
        request=service_request
    )
    essay_list = EssayFill.objects.filter(
        sample__in=service_request.sample_set.all()
    )
    quotation_essays = quotation.essay_fills.all()
    essays_to_add = set(essay_list) - set(quotation_essays)
    quotation.essay_fills.add(*essays_to_add)

    essay_list = quotation.essay_fills.all()
    essay_list = essay_list.annotate(
        price=Sum('essaymethodfill__essay_method__price')
    )
    total_price = sum([
        essay.price
        if essay.price else 0
        for essay in essay_list
    ])
    context = {
        'service_request': service_request,
        'essay_list': essay_list,
        'total_price': total_price,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
