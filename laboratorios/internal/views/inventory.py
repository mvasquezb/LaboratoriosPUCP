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
    suplies=Supply.all_objects.filter(deleted__isnull=True)
    equipments=Equipment.all_objects.filter(deleted__isnull=True)
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
        inventory_types= Inventory.TYPE_CHOICES
        context = { 'inventories': inventories,'form': form ,
                    'inventory_types':inventory_types,
                    'supply_list':suplies,'equipments':equipments}
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
                request, 'Se ha editado el inventario exitosamente')
            return redirect('internal:inventory.index')
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
        
        form = InventoryForm()
        context = {'inventory': inventory,
                   'form': form}
        template = 'internal/inventory/show.html'
        return render(request, template, context)

