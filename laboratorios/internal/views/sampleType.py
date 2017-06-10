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
from django.utils.text import slugify

from .forms import SampleTypeForm

NOT_OPTION_SELECTED = "Selecciona una opcion"


def index(request,
          template='internal/sampleType/index.html',
          extra_context=None):
    search = request.GET.get('search')
    if search:
        sampleType_list = SampleType.objects.filter(
            name__icontains=search).order_by('name')
    else:
        sampleType_list = SampleType.objects.order_by('name')

    paginator = Paginator(sampleType_list, 3)
    page = request.GET.get('page')
    try:
        sampletypes = paginator.page(page)
    except PageNotAnInteger:
        sampletypes = paginator.page(1)
    except EmptyPage:
        laboratorys = paginator.page(paginator.num_pages)

    context = {
        'sampleType_list': sampletypes,
        'paginator': paginator,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def validation_name(name):
    return not SampleType.objects.filter(name=name).exists()


def create(request,
           template='internal/sampleType/create.html',
           extra_context=None):
    form = SampleTypeForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Registrar Tipos de Muestra'
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Se registró el tipo de muestra con éxito')
            return redirect('internal:sampleType.index')
        else:
            context['errors'] = str(form.errors)
            messages.error(request, 'Ocurrió un error al registrar el tipo de muestra')
    return render(request, template, context)


def edit(request, id, template='internal/sampleType/create.html'):
    sample_type = get_object_or_404(SampleType, pk=id)
    form = SampleTypeForm(request.POST or None, instance=sample_type)
    context = {
        'form': form,
        'page_title': 'Editar Tipo de Muestra',
        'edit': True,
        'sample_type': sample_type,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Se registró el tipo de muestra con éxito')
            return redirect('internal:sampleType.index')
        else:
            context['errors'] = str(form.errors)
            messages.error(request, 'Ocurrió un error al registrar el tipo de muestra')
    return render(request, template, context)


def delete(request,
           id,
           template='internal/sampleType/index.html',
           extra_context=None):
    sample_type = get_object_or_404(SampleType, pk=id)
    if request.method == 'POST':
        sample_type.delete()
    return redirect('internal:sampleType.index')
