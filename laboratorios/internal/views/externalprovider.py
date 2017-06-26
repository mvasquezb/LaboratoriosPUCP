from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages

from internal import models
from internal.views.forms import ExternalProviderForm


def index(request,
          template='internal/externalprovider/index.html',
          extra_context=None):
    provider_list = models.ExternalProvider.all_objects.filter(
        deleted__isnull=True
    )
    context = {
        'provider_list': provider_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         id,
         template='internal/externalprovider/show.html',
         extra_context=None):
    provider = get_object_or_404(models.ExternalProvider.all_objects.filter(
        deleted__isnull=True,
    ), pk=id)
    context = {
        'provider': provider,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def edit(request,
         id,
         template='internal/externalprovider/edit.html',
         extra_context=None):
    provider = get_object_or_404(models.ExternalProvider.all_objects.filter(
        deleted__isnull=True,
    ), pk=id)
    form = ExternalProviderForm(request.POST or None, instance=provider)
    if request.method == 'POST':
        if form.is_valid():
            provider = form.save()
            return redirect('internal:externalprovider.index')
    context = {
        'provider': provider,
        'provider_form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def delete(request, id):
    provider = get_object_or_404(models.ExternalProvider.all_objects.filter(
        deleted__isnull=True,
    ), pk=id)
    provider.delete()
    messages.success(request, 'Se eliminó el proveedor exitosamente')
    return redirect('internal:externalprovider.index')
