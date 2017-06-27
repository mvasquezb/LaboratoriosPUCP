from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages

from internal import models
from internal.views.forms import ExternalProviderForm
from internal.permissions import user_passes_test
from internal.permissions.externalprovider import *


@user_passes_test(index_externalprovider_check, login_url='internal:index')
def index(request,
          template='internal/externalprovider/index.html',
          extra_context=None):
    provider_list = models.ExternalProvider.all_objects.all()
    context = {
        'provider_list': provider_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(show_externalprovider_check, login_url='internal:index')
def show(request,
         id,
         template='internal/externalprovider/show.html',
         extra_context=None):
    provider = get_object_or_404(models.ExternalProvider.all_objects, pk=id)
    service_list = models.ServiceRequest.all_objects.filter(
        external_provider=provider
    )
    context = {
        'provider': provider,
        'service_list': service_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(create_externalprovider_check, login_url='internal:index')
def create(request,
           template='internal/externalprovider/create.html',
           extra_context=None):
    form = ExternalProviderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            provider = form.save()
            messages.success(request, 'Se registró el proveedor exitosamente')
            return redirect('internal:externalprovider.index')
        else:
            for field in form:
                if field.errors:
                    msg = field.label + ': ' + str(field.errors)
                    messages.error(request, msg)
    context = {
        'provider_form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(edit_externalprovider_check, login_url='internal:index')
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
            messages.success(request, 'Se registró el proveedor exitosamente')
            return redirect('internal:externalprovider.index')
        else:
            for field in form:
                if field.errors:
                    msg = field.label + ': ' + str(field.errors)
                    messages.error(request, msg)
    context = {
        'provider': provider,
        'provider_form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(delete_externalprovider_check, login_url='internal:index')
def delete(request, id):
    provider = get_object_or_404(models.ExternalProvider.all_objects.filter(
        deleted__isnull=True,
    ), pk=id)
    provider.delete()
    messages.success(request, 'Se eliminó el proveedor exitosamente')
    return redirect('internal:externalprovider.index')
