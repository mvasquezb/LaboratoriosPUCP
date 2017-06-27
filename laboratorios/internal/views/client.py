from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from django.urls import *
from internal.models import *
from internal.views.forms import *
from internal import utils
from internal.permissions import user_passes_test
from internal.permissions.client import *


def index(request,
          template='internal/client/index.html',
          extra_context=None):
    client_list = Client.all_objects.order_by('user__username')

    context = {
        'clients_list': client_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         pk,
         template='internal/client/show.html'):
    client = get_object_or_404(Client, pk=pk)
    user_form = UserEditForm(request.POST or None, instance=client.user)
    form = ClientForm(request.POST or None, instance=client)
    context = {
        'custom_client': client,
        'form' : form,
        'user_form': user_form
    }
    return render(request, template, context)


def create(request,
                  template='internal/client/create.html'):
    user_form = UserCreationForm(request.POST or None)
    form = ClientForm(request.POST or None)
    context = {
        'form': form,
        'user_form': user_form,
    }
    if request.method == 'POST':
        if user_form.is_valid() and form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            new_client = form.save()
            messages.success(
                request,
                'Se ha creado el empleado exitosamante!'
            )

            return redirect('internal:client.index')
        else:
            # Show errors
            print(user_form.errors, form.errors)
            pass
    return render(request, template, context)


def edit(request,
        pk,
        template='internal/client/edit.html'):

    client = get_object_or_404(Client, pk=pk)
    user_form = UserEditForm(request.POST or None, instance=client.user)
    form = ClientForm(request.POST or None, instance=client)
    context = {
        'form': form,
        'client': client,
        'user_form': user_form,
    }
    if request.method == 'POST':
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            messages.success(request, 'Se ha editado el cliente exitosamante!')
            return redirect('internal:client.index')
        else:
            print(user_form.errors, form.errors)
            messages.warning(request, 'Corrija los errores.')
    return render(request, template, context)


def delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()

    return redirect('internal:client.index')