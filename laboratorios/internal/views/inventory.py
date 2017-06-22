from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count

from internal.models import *
from .forms import InventoryForm
import json as simplejson


def index(request,
          template='internal/inventory/index.html',
          extra_context=None):
    inventorys = Inventory.all_objects.all()
    context = {
        'inventorys_list': inventorys
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)



def create(request,
           template='internal/inventory/create.html',
           extra_content=None):
    form = InventoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Se ha creado un nuevo inventario exitosamante!')
            return redirect('internal:inventory.index')
        else:
            for field, errors in form.errors.items():
                if (field == "name") and list(errors) == ['Ya existe inventory con este Name.']:
                    messages.error(
                        request, 'Este nombre de inventario ya existe, pruebe otro')
                    return redirect('internal:inventory.create')
    else:
        inventories = Inventory.all_objects.filter(deleted__isnull=True)
        context = { 'inventories': inventories,'form': form }
        return render(request, template, context)


def edit(request,
         pk):
    if request.method == 'POST':
        instance = Inventory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        aux_form = InventoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
            aux_form.save()
            messages.success(
                request, 'Se ha editado el inventario exitosamante')
            return redirect('internal:inventory.index')
        else:
            messages.error(
                request, 'Ya existe un inventario con el mismo nombre, ingrese otro')
            return redirect('internal:inventory.edit', pk=pk)
    else:
        instance = Inventory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        form = InventoryForm()
        inventories = Inventory.all_objects.filter(deleted__isnull=True)
        context = { 'inventories': inventories,'form': form , 'inventory':instance}
        template = 'internal/inventory/edit.html'
        return render(request, template, context)


def delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, 'Se ha borrado el inventario existosamente')
    return redirect('internal:inventory.index')


def show(request,
         pk):
    if request.method == 'POST':
        instance = inventory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        aux_form = InventoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
            aux_form.save()
            return redirect('internal:inventory.index')
    else:
        inventory = inventory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        #
        all_users = Employee.all_objects.filter(deleted__isnull=True)
        selected_users = inventory.employees.all()
        #
        all_service_hours = inventoryServiceHours.all_objects.filter(
            deleted__isnull=True
        )
        selected_service_hours = inventory.service_hours
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = inventory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = inventory.essay_methods.all()
        #
        form = InventoryForm()
        context = {'inventory': inventory, 'all_users': all_users,
                   'selected_users': selected_users, 'all_service_hours': all_service_hours,
                   'selected_service_hours': selected_service_hours,
                   'all_inventories': all_inventories, 'selected_inventories': selected_inventories,
                   'all_essaymethods': all_essaymethods, 'selected_essaymethods': selected_essaymethods,
                   'form': form}
        template = 'internal/inventory/show.html'
        return render(request, template, context)

