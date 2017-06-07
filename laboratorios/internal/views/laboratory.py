from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from internal.models import *


def index(request,
          template='internal/laboratory/index.html',
          extra_context=None):
    search = request.GET.get('search')
    if search:
        laboratory_list = Laboratory.objects.filter(
            name__icontains=search).order_by ('name')
    else:
        laboratory_list = Laboratory.objects.order_by ('name')

    paginator = Paginator(laboratory_list, 3)
    page = request.GET.get('page')
    try:
        laboratorys = paginator.page (page)
    except PageNotAnInteger:
        laboratorys = paginator.page(1)
    except EmptyPage:
        laboratorys = paginator.page(paginator.num_pages)

    context = {
        'laboratorys_list': laboratorys,
        'paginator': paginator,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def create(request,
           template='internal/laboratory/create.html',
           extra_content=None):
    users = Laboratory.objects.all ()
    context = {'users': users}
    return render(request, template, context)
