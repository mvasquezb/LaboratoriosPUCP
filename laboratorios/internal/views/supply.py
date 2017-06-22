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
from django.contrib.auth.decorators import login_required
from internal.views.forms import (
    EmployeeForm,
    UserCreationForm,
    UserEditForm,
    SupplyForm
)


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


def delete(request, pk):
    supply= get_object_or_404(Supply, pk=pk)
    supply.delete()

    return redirect('internal:supply.index')
