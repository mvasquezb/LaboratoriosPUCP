from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from internal.models import *
from django.utils.text import slugify
from .forms import SampleTypeForm
from internal.permissions import user_passes_test
from internal.permissions.sampleType import *

NOT_OPTION_SELECTED = "Selecciona una opcion"


@user_passes_test(index_sample_type_check, login_url='internal:index')
def index(request,
          template='internal/sampleType/index.html',
          extra_context=None):
    sample_types = SampleType.objects.order_by('name')

    context = {
        'sample_types': sample_types,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def validation_name(name):
    return not SampleType.objects.filter(name=name).exists()


@user_passes_test(create_sample_type_check, login_url='internal:index')
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


@user_passes_test(edit_sample_type_check, login_url='internal:index')
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


@user_passes_test(delete_sample_type_check, login_url='internal:index')
def delete(request,
           id,
           template='internal/sampleType/index.html',
           extra_context=None):
    sample_type = get_object_or_404(SampleType, pk=id)
    if request.method == 'POST':
        sample_type.delete()
    return redirect('internal:sampleType.index')
