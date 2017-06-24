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
from django.contrib.auth.decorators import user_passes_test
from internal.views.forms import (
    UserCreationForm,
    UserEditForm,
    EquipmentForm
)
from internal.permissions.equipment import *


def index(request,
          template='internal/equipment/index.html',
          extra_context=None):
    equipment_list = Equipment.objects.order_by('registered_date')

    context = {
        'equipment_list': equipment_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         pk,
         template='internal/equipment/show.html'):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None)
    context = {
        'form': form,
        'equipment': equipment,
    }
    return render(request, template, context)


@user_passes_test(create_equipment_check, login_url='internal:index')
def create(request,
           template='internal/equipment/create.html'):
    #user_form = UserCreationForm(request.POST or None)
    form = EquipmentForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Se ha creado el equipo exitosamante!'
            )
            return redirect('internal:equipment.index')
        else:
            # Show errors
            pass
    return render(request, template, context)


@user_passes_test(edit_equipment_check, login_url='internal:index')
def edit(request, pk,
         template='internal/equipment/edit.html'):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=equipment)
    context = {
        'form': form,
        'equipment': equipment,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha editado el equipo exitosamante!')
            return redirect('internal:equipment.index')
        else:
            messages.warning(request, 'Corregir los errores mostrados.')
    return render(request, template, context)


@user_passes_test(delete_equipment_check, login_url='internal:index')
def delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()

    return redirect('internal:equipment.index')
