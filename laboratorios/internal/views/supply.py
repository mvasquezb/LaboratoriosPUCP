from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from internal.models import *
from internal.views.forms import (
    SupplyForm,
)
from internal.permissions import user_passes_test
from internal.permissions.supply import *


@user_passes_test(index_supply_check, login_url='internal:index')
def index(request,
          template='internal/supply/index.html',
          extra_context=None):
    supply_list = Supply.objects.order_by('registered_date')

    context = {
        'supply_list': supply_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(show_supply_check, login_url='internal:index')
def show(request,
         pk,
         template='internal/supply/show.html'):
    supply = get_object_or_404(Supply, pk=pk)
    form = SupplyForm(request.POST or None)
    context = {
        'form': form,
        'supply': supply,
    }
    return render(request, template, context)


@user_passes_test(create_supply_check, login_url='internal:index')
def create(request,
           template='internal/supply/create.html'):
    #user_form = UserCreationForm(request.POST or None)
    form = SupplyForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Se ha creado el suministro exitosamante!'
            )
            return redirect('internal:supply.index')
        else:
            # Show errors
            pass
    return render(request, template, context)


@user_passes_test(edit_supply_check, login_url='internal:index')
def edit(request, pk,
         template='internal/supply/edit.html'):
    supply = get_object_or_404(Supply, pk=pk)
    form = SupplyForm(request.POST or None, instance=supply)
    context = {
        'form': form,
        'supply': supply,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha editado el suministro exitosamante!')
            return redirect('internal:supply.index')
        else:
            messages.warning(request, 'Corregir los errores mostrados.')
    return render(request, template, context)


@user_passes_test(delete_supply_check, login_url='internal:index')
def delete(request, pk):
    supply= get_object_or_404(Supply, pk=pk)
    supply.delete()

    return redirect('internal:supply.index')
